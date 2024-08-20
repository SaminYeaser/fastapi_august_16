from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashingPassword(password):
    
    return pwd_context.hash(password)

def verfiyPassword(plainPassword,hashPassword):
    return pwd_context.verify(plainPassword, hashPassword)