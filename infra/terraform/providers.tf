terraform {
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.8.0"
    }
    vercel = {
      source  = "vercel/vercel"
      version = "~> 5.4.1"
    }
  }
}

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

provider "vercel" { api_token = var.vercel_api_token }