provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "thinkalike" {
  name     = "thinkalike-rg"
  location = "East US"
}

resource "azurerm_app_service" "thinkalike_app" {
  name                = "thinkalike-app"
  location            = azurerm_resource_group.thinkalike.location
  resource_group_name = azurerm_resource_group.thinkalike.name
  app_service_plan_id = azurerm_app_service_plan.thinkalike_plan.id
}
