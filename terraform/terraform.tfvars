aws_region  = "us-east-1"
profile = "bala-us-east"
CIDR_blocks = [
    { name="vpc0_cidr_block", cidr_block= "10.0.0.0/16" },
    { name="subnet0_cidr_block", cidr_block="10.0.1.0/24" }
]
environment = "cloud-switcher"  
avail_zone = "us-east-1a"
env_prefix = "cloud-switcher"
AVAILIBILITY_zones = ["us-east-1a","us-east-1b","us-east-1c"]
vpc_cidr_block = "10.0.0.0/16"
subnet_cidr_block = "10.0.2.0/24"
my_ip = "84.69.235.33/32"
aws_instance_type = "t2.micro"
public_key_location = "./keys/python-django.pub"
 
