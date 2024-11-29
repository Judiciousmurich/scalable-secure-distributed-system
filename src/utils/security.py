import ssl
import socket
import uuid
import hashlib
import secrets
import logging
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

def generate_client_credentials():
    """Generate unique client identifier"""
    return str(uuid.uuid4())

def generate_ssl_certificate(common_name='localhost'):
    """
    Generate a self-signed SSL certificate
    
    Args:
        common_name (str): Common name for the certificate
    
    Returns:
        Tuple of certificate and private key file paths
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Prepare subject and issuer information
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"KE"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Nairobi"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Nairobi"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Distributed Systems"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])

        # Create the certificate
        certificate = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).sign(private_key, hashes.SHA256())

        # Write private key
        with open("server.key", "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Write certificate
        with open("server.crt", "wb") as cert_file:
            cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))

        logger.info("SSL certificate generated successfully")
        return "server.key", "server.crt"

    except Exception as e:
        logger.error(f"Certificate generation failed: {e}")
        raise

def secure_hash(data):
    """Create a secure hash of input data"""
    return hashlib.sha256(str(data).encode()).hexdigest()

def generate_secure_token(length=32):
    """Generate a cryptographically secure random token"""
    return secrets.token_hex(length // 2)

def verify_ssl_certificate(cert_path):
    """
    Basic verification of SSL certificate
    
    Args:
        cert_path (str): Path to certificate file
    
    Returns:
        bool: Certificate validity
    """
    logger = logging.getLogger(__name__)
    
    try:
        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            certificate = x509.load_pem_x509_certificate(cert_data)
        
        # Check certificate expiration
        current_time = datetime.utcnow()
        if current_time < certificate.not_valid_before or current_time > certificate.not_valid_after:
            logger.warning("Certificate is expired or not yet valid")
            return False
        
        logger.info("Certificate validation successful")
        return True
    
    except Exception as e:
        logger.error(f"Certificate verification failed: {e}")
        return False