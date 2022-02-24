# The VPC that spans across multiple availability zones.
#
# Given the CIDR 10.0.0.0/16, we can have IPs from 10.0.0.1
# up to 10.0.255.254. Essentially we can host 65k IPs in
# that range. 
resource "aws_vpc" "main" {
  cidr_block           = "${var.cidr}"
  enable_dns_hostnames = true
}

# Internet gateway to give our VPC access to the outside world
resource "aws_internet_gateway" "main" {
  vpc_id = "${aws_vpc.main.id}"
}

# Grant the VPC internet access by creating a very generic
# destination CIDR ("catch all" - the least specific possible) 
# such that we route traffic to outside as a last resource for 
# any route that the table doesn't know about.
resource "aws_route" "internet_access" {
  route_table_id         = "${aws_vpc.main.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.main.id}"
}

# Creates N subnets according to the subnet mapping described in
# the `az-subnet-mapping` variable.
#
# The variable is a list of maps in the following form:
#
#   [  { name: "crazydog", az: "name-of-the-az", cidr: "cidr-range" } , ... ]
#
# For instance:
#
#   [ { name =  "sub1", az = "us-east-1a", cidr = "192.168.0.0/24"  } ]
#
resource "aws_subnet" "main" {
  count = "${length(var.az-subnet-mapping)}"

  cidr_block              = "${lookup(var.az-subnet-mapping[count.index], "cidr")}"
  vpc_id                  = "${aws_vpc.main.id}"
  map_public_ip_on_launch = true
  availability_zone       = "${lookup(var.az-subnet-mapping[count.index], "az")}"

  tags = {
    Name = "${lookup(var.az-subnet-mapping[count.index], "name")}"
  }
}
