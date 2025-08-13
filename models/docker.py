from pydantic import BaseModel, Field


class DockerImage(BaseModel):
    image_name: str = Field(
        description="Docker image name with optional tag (e.g., 'supurr/algotrade:0.2')"
    )
