from function_support import *

# đường dẫn đến file ảnh đã mã hóa
path_Name = "Encrypt.png"

# tên file ảnh đã được mã hóa
save_file = "Decrypt.png"

# phần dư khi lưu khi chia cho 256 để đưa mã màu về khoảng [0,255]
quotient = "quotient.txt"
if __name__ == "__main__":
    img = Decrypted(path_ImageDecode=path_Name, path_private_key="rsa.txt", save_imageDecrypted=save_file, path_file_quotient=quotient)

    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
