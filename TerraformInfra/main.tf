terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "OpenSource" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_virtual_network" "vn-OpenSource" {
  name                = "vn-OpenSource"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.OpenSource.location
  resource_group_name = azurerm_resource_group.OpenSource.name
}

resource "azurerm_subnet" "s-OpenSource" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.OpenSource.name
  virtual_network_name = azurerm_virtual_network.vn-OpenSource.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_public_ip" "ip-vm1" {
  name                = "internal"
  location            = azurerm_resource_group.OpenSource.location
  resource_group_name = azurerm_resource_group.OpenSource.name
  allocation_method   = "Dynamic"
}


resource "azurerm_network_interface" "nic-vm1" {
  name                = "NIC_vm1"
  location            = azurerm_resource_group.OpenSource.location
  resource_group_name = azurerm_resource_group.OpenSource.name
  lifecycle {
    create_before_destroy = true
  }

  ip_configuration {
    name = "conf_internal_vm1"
    private_ip_address_allocation = "Dynamic"
    subnet_id = azurerm_subnet.s-OpenSource.id
    public_ip_address_id = azurerm_public_ip.ip-vm1.id
  } 
}


resource "azurerm_network_security_group" "nsg-OpenSource" {
  name                = "acceptanceTestSecurityGroup1"
  location            = azurerm_resource_group.OpenSource.location
  resource_group_name = azurerm_resource_group.OpenSource.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "22"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    environment = "Production"
  }
}

resource "azurerm_linux_virtual_machine" "vm1" {
  name                = var.vm1_name
  resource_group_name = azurerm_resource_group.OpenSource.name
  location            = azurerm_resource_group.OpenSource.location
  size                = var.vm1_size
  admin_username = var.vm1_username
  custom_data = filebase64("Scripts/GetAnsibleReady.yaml")
  network_interface_ids = [
    azurerm_network_interface.nic-vm1.id,
  ]

  admin_ssh_key {
    username = var.vm1_username
    public_key = file("/path/to/public/key.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = var.vm1_os_publisher
    offer     = var.vm1_os_offer
    sku       = var.vm1_os_sku
    version   = var.vm1_os_version
  }
}
