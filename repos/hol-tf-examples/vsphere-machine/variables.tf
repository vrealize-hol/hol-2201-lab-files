variable "vsphere_datacenter" {
  type = string
  default = "RegionA01"
}

variable "vsphere_resource_pool" {
  type = string
  default = "Workload 1/Resources"
}

variable "vsphere_datastore" {
  type = string
  default = "RegionA01-ISCSI01-COMP01"
}

variable "vm_template" {
  type = string
  default = "ubuntu18"
}

variable "vm_hostname" {
  type = string
}

variable "vm_cpu_count" {
  type = string
}

variable "vm_ram_count" {
  type = string
}

variable "vm_linked_clone" {
  type = bool
  default = false
}

variable "vsphere_network" {
  type = string
  default = "VM-RegionA01-vDS-COMP"
}

variable "vm_domain" {
  type = string
  default = "corp.local"
}

variable "vm_ipv4_address" {
  type = string
}

variable "vm_ipv4_netmask" {
  type = string
}

variable "vm_ipv4_gateway" {
  type = string
}