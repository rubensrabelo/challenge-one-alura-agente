terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.8.0"
    }
  }
}

resource "render_web_service" "api" {
  name           = var.service_name
  plan           = "free"
  region         = "oregon"
  root_directory = "app/backend"

  runtime_source = {
    docker = {
      auto_deploy     = true
      branch          = "main"
      repo_url        = "https://github.com/${var.github_repo}"
      dockerfile_path = "Dockerfile"
    }
  }

  env_vars = {
    HUGGINGFACEHUB_API_TOKEN = {
      value = var.huggingface_api_token
    }
    PORT = {
      value = "8000"
    }
    HOST = {
      value = "0.0.0.0"
    }
  }
}
