#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <stdlib.h>

using namespace std;

int main()
{
	fstream file; string pre_path,path; smatch mat;
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
	system((string("explorer.exe ") + path).c_str());
	return 0;
}
