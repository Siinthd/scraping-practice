from  steganocryptopy.steganography import Steganography
from stegano import lsb

Steganography.generate_key('')
secret = Steganography.encrypt('key.key','images/test.png','TODO.txt')
secret.save('images/test1.png')

decrypt1 = Steganography.decrypt('key.key','images/splat1.png')
print(decrypt1)


secret = lsb.hide("images/cat1.png", "Hello world!")
secret.save("images/cat11.png")
print(lsb.reveal("images/cat11.png"))
