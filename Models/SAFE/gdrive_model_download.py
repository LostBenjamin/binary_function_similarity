#!/usr/bin/env python
# coding: utf-8

##############################################################################
#                                                                            #
#  Code for the USENIX Security '22 paper:                                   #
#  How Machine Learning Is Solving the Binary Function Similarity Problem.   #
#                                                                            #
#  MIT License                                                               #
#                                                                            #
#  Copyright (c) 2019-2022 Cisco Talos                                       #
#                                                                            #
#  Permission is hereby granted, free of charge, to any person obtaining     #
#  a copy of this software and associated documentation files (the           #
#  "Software"), to deal in the Software without restriction, including       #
#  without limitation the rights to use, copy, modify, merge, publish,       #
#  distribute, sublicense, and/or sell copies of the Software, and to        #
#  permit persons to whom the Software is furnished to do so, subject to     #
#  the following conditions:                                                 #
#                                                                            #
#  The above copyright notice and this permission notice shall be            #
#  included in all copies or substantial portions of the Software.           #
#                                                                            #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,           #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF        #
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                     #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE    #
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION    #
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION     #
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.           #
#                                                                            #
#  gdrive_model_download.py - Download the model from Google Drive           #
#                                                                            #
##############################################################################

import gdown
import hashlib
import os
import zipfile

MODELS_DICT = {
    "NeuralNetwork/model_checkpoint.zip":
    "1SPYsR5Is8IJVTPNpStCdX7ibx-G3E2G3",
    "Pretraining/instruction_embeddings.zip":
    "1A7STkuH3uQy_8WJlPwU6YM2MQoxf-3HV"
}

SHA256_DICT = {
    "NeuralNetwork/model_checkpoint.zip":
    "7699e824cacfe2d6590b8b569a6240a0905b46cd1e68d311259cc43e5373dfa1",
    "Pretraining/instruction_embeddings.zip":
    "528751f367e321a956b5c07c32822cf617e85a547e979e07a47da6a9aef00806"
}


def compute_sha256(file_path):
    """Compute the sha256 for the file in file_path."""
    blocksize = 65536
    sha = hashlib.sha256()
    with open(file_path, 'rb') as f_in:
        file_buffer = f_in.read(blocksize)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            file_buffer = f_in.read(blocksize)
    return sha.hexdigest()


def download_safe_model_data():
    """Download the model data from Google Drive."""
    try:
        for zip_name, gid in MODELS_DICT.items():
            temp_dir = zip_name.split(".")[0]
            if os.path.isdir(temp_dir):
                print("[W] {} already exists".format(temp_dir))
                continue

            zip_path = zip_name
            print("Downloading {} ...".format(zip_name))
            gdown.download(id=gid, output=zip_path, quiet=False)

            if not os.path.isfile(zip_path):
                print("[!] Error: file {} not found".format(zip_path))
                continue

            print("Checking checksum {} ...".format(zip_name))
            sha = compute_sha256(zip_path)
            if sha != SHA256_DICT[zip_name]:
                print("[!] Checksum error: {} != {}".format(
                    sha, SHA256_DICT[zip_name]))
                continue

            print("Extracting archive...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(zip_path))

            os.remove(zip_path)
            print()

    except Exception as e:
        print("[!] Exception in download_safe_model_data\n{}".format(e))


def main():
    download_safe_model_data()
    print("That's all")


if __name__ == "__main__":
    main()
