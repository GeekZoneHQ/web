terraform {
  required_version = ">= 0.12"

  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "geekzone"

    workspaces {
      name = "cicd-ec2"
    }
  }
}

provider "aws" {
  region=var.aws_region
}
 
// vpc
resource "aws_vpc" "gz-vpc" {
    cidr_block = var.vpc_cidr_block
    tags = {
        Name = "${var.env_prefix}-vpc"
    }
}


resource "aws_internet_gateway" "dev_demo_igw" {
    vpc_id = aws_vpc.gz-vpc.id
    tags = {
        Name = "${var.env_prefix}-igw"
    }    
} 


// subnet
resource "aws_subnet" "my-dev-subnet-1" {
    vpc_id = aws_vpc.gz-vpc.id
    cidr_block = var.subnet_cidr_block
    tags = {        
        Name = "${var.env_prefix}-subnet-1"
    }
    availability_zone = var.avail_zone 
}


resource "aws_route_table" "dev_demo_route_table"{
    vpc_id = aws_vpc.gz-vpc.id
    route {
        cidr_block  = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.dev_demo_igw.id
    }
    tags = {
        Name = "${var.env_prefix}-rtb"
    }
}

resource "aws_route_table_association" "a-rtb-subnet" { 
    subnet_id = aws_subnet.my-dev-subnet-1.id
    route_table_id = aws_route_table.dev_demo_route_table.id
}


# Create a security group 
resource "aws_security_group" "allow-ssh-and-egress" {
    name = "main"
    description = "Allows SSH traffic into instances as well as all egress."
    vpc_id = aws_vpc.gz-vpc.id
    ingress{
        from_port = 22
        to_port= 22
        protocol = "tcp"
        cidr_blocks = [var.my_ip]
        
    }


    // allow any traffic outside
    egress{
        from_port = 0
        to_port= 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
        prefix_list_ids = []
    }

    tags = {
        Name = "${var.env_prefix}-sg"
    }
}




data "cloudinit_config" "gz_cloudinit" {
  part {
    content_type = "text/x-shellscript"
    content      = file("./deploy/templates/user-data.sh")
  }

  part {
    content_type = "text/cloud-config"
    content = yamlencode({
      write_files = [
        {
          encoding    = "b64"
          content     = filebase64("./deploy/templates/ec2-caller.sh")
          path        = "/home/ubuntu/ec2-caller.sh"
          owner       = "ubuntu:ubuntu"
          permissions = "0755"
        },
      ]
    })
  }
}


/*
  provision an ec2 instance and will need to  trigger the circleci
*/
resource "aws_instance" "gz_instance" {
  ami           = data.aws_ami.ubuntu.id  
  instance_type = var.aws_instance_type       
  key_name = aws_key_pair.main.key_name
  subnet_id = aws_subnet.my-dev-subnet-1.id
  vpc_security_group_ids = [aws_security_group.allow-ssh-and-egress.id]
  availability_zone = var.avail_zone
  associate_public_ip_address = false
  user_data     = data.cloudinit_config.gz_cloudinit.rendered
  tags ={
    Name = "$K8S_NS_NAME"
  }
}





