#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <stdlib.h>
#include <tchar.h>
#include <atlstr.h>
#include <Windows.h>

using namespace std;

bool ExtractResource(LPCTSTR strDstFile, LPCTSTR strResName, LPCTSTR strResType)
{
    // 创建文件
    HANDLE FileHandle = ::CreateFile(strDstFile, GENERIC_WRITE, NULL, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (FileHandle == INVALID_HANDLE_VALUE)
        return false;

    // 查找资源文件中、加载资源到内存、得到资源大小
    HRSRC    hRes = ::FindResource(NULL, strResName, strResType);
    HGLOBAL  hMem = ::LoadResource(NULL, hRes);
    DWORD    dwSize = ::SizeofResource(NULL, hRes);

    // 写入文件
    DWORD dwWrite = 0; // 返回写入字节
    ::WriteFile(FileHandle, hMem, dwSize, &dwWrite, NULL);
    ::CloseHandle(FileHandle);

	return true;
}

int main()
{
    fstream file; string pre_path, path = "Empty"; smatch mat;
	file.open(getenv("appdata") + string("/../Local/ReadyOrNot/Saved/Logs/Modio.log"), ios::in);
	while (getline(file, pre_path))
	{
		if (regex_search(pre_path, mat, *(new regex("ReadyOrNot"))))
		{       
			for (sregex_iterator pos(pre_path.cbegin(), pre_path.cend(), *(new regex("[A-Z]:\.+Paks"))), end; pos != end; pos++)
			{
				path = pos->str();
			}
		}
	}
	file.close();
    string FILE_NAME = "\\pakchunk999-Mods_R18G_CH_Localization_P.pak";
	auto Fucking_Converter = CString((path + FILE_NAME).c_str());
	ExtractResource(Fucking_Converter, MAKEINTRESOURCE(101), _T("Pak"));
	if (path.compare(string("Empty")) != 0)
	{
		printf("汉化补丁释放成功，进入游戏即可切换语言至中文。\n");
	}
	else
	{
		printf("你尚未启动过游戏或是游戏安装路径包含中文，在这种情况下游戏Log不存在/不包含可查找的安装路径，安装失败 :(\n");
	}
	system("pause");
	//system((string("explorer.exe ") + path).c_str());
	return 0;
}
