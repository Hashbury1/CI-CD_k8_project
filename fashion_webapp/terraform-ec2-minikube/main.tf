terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Specify a suitable AWS provider version
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "minikube_inst" {
  ami                    = "ami-0de716d6197524dd9"
  instance_type          = "t3.medium"
  key_name               = "hash-key-East"
  vpc_security_group_ids = [aws_security_group.minikube_sg.id]
  user_data              = <<-EOF
    #!/bin/bash
    sudo apt update
    sudo apt install -y curl wget apt-transport-https gnupg
    curl -fsSL https://kubernetes.io/docs/tasks/tools/install-minikube/ | bash
    sudo apt install -y docker.io
    sudo usermod -aG docker $USER
    sudo systemctl start docker
    minikube start --driver=docker --container-runtime=docker
  EOF

  tags = {
    Name = "MinikubeInst"
  }
}

resource "aws_security_group" "minikube_sg" {
  name        = "SG-minikube"
  description = "Allow SSH and all internal traffic for Minikube"
  vpc_id      = data.aws_vpc.default.id


  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp" # All protocols
    cidr_blocks = ["129.222.206.136/32"]
  }

  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow outbound HTTP traffic"
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow outbound HTTPS traffic"
  }

}

data "aws_vpc" "default" {
  default = true
}

output "public_ip" {
  value       = aws_instance.minikube_inst.public_ip
  description = "The public IP address of the EC2 instance"
}