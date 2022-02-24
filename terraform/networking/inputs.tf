variable "az-subnet-mapping" {
  description = "Lists the subnets to be created in their respective AZ."
  type        = list 
}

variable "cidr" {
  description = "CIDR block to assign to the VPC"
  type        = string
}
