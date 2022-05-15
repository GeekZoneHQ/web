variable "aws_region" {
    description = "AWS region"
    default = "eu-west-2"
    type = string
}



variable "profile" {
  description = "Profile with permissions to provision the AWS resources."
  default     = "bala"
}

variable vpc_cidr_block {}
variable public_key_location{}
variable avail_zone {}


variable subnet_cidr_block {}

variable my_ip{}


variable aws_instance_type{}

variable "CIDR_blocks"{
    description = " list of CIDR blocks, vpc, subnet0, subnet 1,subnet 2"
    type = list(object({
        name = string
        cidr_block = string        
    }))
}



variable "AVAILIBILITY_zones"{
    description = "list of the availability_zones"
    type = list(string)
}

variable "environment"{
    description = "holds the value of the current environment - dev,staging,prod"
    default = "dev"
    type = string
}

variable "env_prefix"{}



