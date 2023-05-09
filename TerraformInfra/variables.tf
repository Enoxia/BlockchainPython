variable "resource_group_name" {
  type    = string
  default = "OpenSource"
}

variable "location" {
  type    = string
  default = "francecentral"
}


# Virtual Machine 1

variable "vm1_name" {
  type    = string
  default = "Chewbacca"
}

variable "vm1_size" {
  type    = string
  default = "Standard_B1s"
}

variable "vm1_os_publisher" {
  type    = string
  default = "Debian"
}

variable "vm1_os_offer" {
  type    = string
  default = "debian-10"
}

variable "vm1_os_sku" {
  type    = string
  default = "10"
}

variable "vm1_os_version" {
  type    = string
  default = "latest"
}

variable "vm1_username" {
  type    = string
  default = "Bailly"
}
