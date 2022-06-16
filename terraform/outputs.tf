 
output "ec2_public_ip" {
    value = aws_instance.gz_instance.public_ip
}


output "dev_vpc_id"{
    value = aws_vpc.gz-vpc.id
}

output "subnet-1-id" {
    value = aws_subnet.my-dev-subnet-1.id
}



