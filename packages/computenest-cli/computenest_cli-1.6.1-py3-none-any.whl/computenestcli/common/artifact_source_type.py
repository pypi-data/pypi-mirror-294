from enum import Enum, auto


class ArtifactSourceType(Enum):
    """
    部署物源类型，包括：源代码、安装包、Dockerfile、DockerCompose、HelmChart、无部署物
    """
    SOURCE_CODE = 'SourceCode'
    INSTALL_PACKAGE = 'InstallPackage'
    DOCKERFILE = 'Dockerfile'
    DOCKER_COMPOSE = 'DockerCompose'
    HELM_CHART = 'HelmChart'
    NO_ARTIFACT = 'NoArtifact'
