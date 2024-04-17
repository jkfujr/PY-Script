from OpenSSL import crypto

def convert_cer_to_crt(cer_path, crt_path):
    try:
        # 读取cer证书内容
        with open(cer_path, 'rb') as cer_file:
            cer_data = cer_file.read()

        # 尝试使用PEM格式加载证书
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cer_data)

        # 写入crt证书
        with open(crt_path, 'wb') as crt_file:
            crt_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
        print(f"成功将 {cer_path} 转换为 {crt_path}")
    except Exception as e:
        print(f"转换失败：{e}")

if __name__ == "__main__":
    # 输入cer证书和要保存的crt证书路径
    cer_file_path = input("请输入cer证书的路径：")
    crt_file_path = input("请输入要保存的crt证书的路径：")

    # 执行转换
    convert_cer_to_crt(cer_file_path, crt_file_path)
