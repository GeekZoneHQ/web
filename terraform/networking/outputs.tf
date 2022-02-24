# Creates a mapping between subnet name and generated subnet ID.
#
# Given an `aws_subnet` resource created with `count`, we can access
# properties from the list of resources created as a list by using
# the wildcard syntax:
# 
#     <resource>.*.<property>
#
# By making use of `zipmap` we can take two lists and create a map
# that uses the values from the first list as keys and the values
# from the seconds list as values.
#
output "az-subnet-id-mapping" {
  description = "maps subnet name and AWS subnet ID"
  value       = "${zipmap(aws_subnet.main.*.tags.Name, aws_subnet.main.*.id)}"
}

output "vpc-id" {
  description = "ID of the generated vpc"
  value       = "${aws_vpc.main.id}"
}

 