import hashlib
import os
from typing import Literal, Optional

from mako.template import Template

from truefoundry.pydantic_v1 import BaseModel


class NotebookImageBuild(BaseModel):
    type: Literal["tfy-notebook-buildpack"] = "tfy-notebook-buildpack"
    base_image_uri: str
    build_script: Optional[str] = None


DOCKERFILE_TEMPLATE = Template(
    """
FROM ${base_image_uri}
USER root

% if build_script_docker_commands is not None:
${build_script_docker_commands}
% endif

USER $NB_UID
"""
)


def generate_build_script_docker_commands(
    build_script: Optional[str], local_dir: str
) -> Optional[str]:
    if not build_script:
        return None
    build_script_path = None
    if build_script:
        # we add build script's hash to the file name to ensure docker cache invalidation
        script_hash = hashlib.sha256(build_script.encode("utf-8")).hexdigest()
        build_script_path = os.path.join(local_dir, f"build-script-{script_hash}.sh")
        with open(build_script_path, "w") as fp:
            fp.write(build_script)
        build_script_path = os.path.relpath(build_script_path, local_dir)
    run_build_script_command = f"""\
COPY {build_script_path} /tmp/user-build-script.sh
RUN mkdir -p /var/log/ && DEBIAN_FRONTEND=noninteractive bash -ex /tmp/user-build-script.sh 2>&1 | tee /var/log/user-build-script-output.log
"""
    return run_build_script_command


def generate_dockerfile_content(
    build_configuration: NotebookImageBuild, local_dir: str
) -> str:
    build_script_docker_commands = generate_build_script_docker_commands(
        build_script=build_configuration.build_script,
        local_dir=local_dir,
    )

    template_args = {
        "base_image_uri": build_configuration.base_image_uri,
        "build_script_docker_commands": build_script_docker_commands,
    }

    template = DOCKERFILE_TEMPLATE

    dockerfile_content = template.render(**template_args)
    return dockerfile_content
