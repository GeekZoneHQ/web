aws_region  = "eu-west-2"
profile = "bala"
CIDR_blocks = [
    { name="vpc0_cidr_block", cidr_block= "10.0.0.0/16" },
    { name="subnet0_cidr_block", cidr_block="10.0.1.0/24" }
]
environment = "dev-demo" // staging, prod
avail_zone = "eu-west-2b"
env_prefix = "dev-demo"
AVAILIBILITY_zones = ["eu-west-2a","eu-west-2b","eu-west-2c"]
vpc_cidr_block = "10.0.0.0/16"
subnet_cidr_block = "10.0.2.0/24"
my_ip = "90.246.79.204/32"
aws_instance_type = "t2.micro"
public_key_location = "./keys/circleci.pub"
 
