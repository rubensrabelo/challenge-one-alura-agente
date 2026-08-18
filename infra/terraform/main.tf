module "render_backend" {
  source       = "./modules/render"
  service_name = "my-python-backend-api"
  github_repo  = var.github_repository
}

module "vercel_frontend" {
  source       = "./modules/vercel"
  project_name = "my-vue-frontend-web"
  github_repo  = var.github_repository
  backend_url  = module.render_backend.service_url
}