//
//  main.c
//  codetemplategen
//
//  Created by Manuel Schreiner on 02.02.19.
//  Copyright © 2019 io-expert.com. All rights reserved.
//

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdarg.h>

#define MALLOC_ZERO(x,siz) x = malloc(siz); memset(x,0,siz)

#if defined(WIN32)
#  define DIR_SEPARATOR '\\'
#  define DIR_SEPARATOR_STRING "\\"
#else
#  define DIR_SEPARATOR '/'
#  define DIR_SEPARATOR_STRING "/"
#endif



extern const char* strTemplateCmakeLists;
extern const char* strDisclaimer;
extern const char* strBuildLinux;
extern const char* strBuildMac;
extern const char* strBuildWindows;
extern const char* strReadme;
extern const char* strVSCodeTasks;
extern const char* strVSCodeLaunch;

char* strCreator = "Joe";
char* strModuleName = "MyModule";
char* strModuleDescription = "My Description";
char* strCompany = NULL;
char* strProjectName = "MyProject";
char* projectname = NULL;
char* strOut = NULL;
char* strIn = NULL;

struct stat st = {0};
char* modulename;
char* MODULENAME;
char* filename_c;
char* filename_h;
bool cppMode = false;
bool isMain = false;
bool genProject = false;
bool txt2c = false;
bool bin2c = false;

const char appname[] = "codetemplategen";
const char* commentHeaderStart =
"/**\r\n"
" *******************************************************************************\r\n";
const char* commentHeaderEnd =
" *******************************************************************************\r\n"
" */\r\n\r\n";

/**
 Write content to file

 @param path Outpath
 @param filename Filename
 @param strContent Content
 @param ... Arguments
 */
void WriteToFile(char* path, char* filename, char* strContent,...)
{
    va_list ap;
    va_start(ap, strContent);
    char filepath[512] = {0};
    strcat(filepath,path);
    strcat(filepath,DIR_SEPARATOR_STRING);
    strcat(filepath,filename);
    FILE *file = fopen(filepath, "w");
    if (file != NULL)
    {
        vfprintf(file,strContent,ap);
        fclose(file);
    }
    va_end(ap);
}

/**
 Write Txt 2 C

 @param path Outpath
 @param txtFile Input Filename
 @param cFile Output Filename
 */
void Txt2C(char* txtFile,char* cFile)
{
    FILE *txtFileHandle = fopen(txtFile, "r");
    FILE *cFileHandle = fopen(cFile, "w");
    char * line = NULL;
    size_t len = 0;
    ssize_t readsz;

    if (txtFileHandle == NULL)
    {
        return;
    }
    if (cFileHandle == NULL)
    {
        return;
    }
    fprintf(cFileHandle,"const char* strFileName = \r\n");
    while ((readsz = getline(&line, &len, txtFileHandle)) != -1) {
        fputc('"',cFileHandle);
        for(int i = 0;i < readsz;i++)
        {
            if (line[i] == '\r')
            {
                //ignore
            }
            else if (line[i] == '\n')
            {
                //ignore    
            }
            else if (line[i] == '%')
            {
                fprintf(cFileHandle,"\\%");
            } else if (line[i] == '\\')
            {
                fprintf(cFileHandle,"\\\\");
            } else if (line[i] == '"')
            {
                fprintf(cFileHandle,"\\\"");
            } else
            {
                fputc(line[i],cFileHandle);
            }
        }
        fprintf(cFileHandle,"\\r\\n\"\r\n");
    }
    fprintf(cFileHandle,";");
    fclose(txtFileHandle);
    fclose(cFileHandle);
}

void Bin2C(char* binFile,char* cFile)
{

}



/**
 Convert a string to lower

 @param strOut Output string pointer
 @param strIn Input string pointer
 */
void StringToLower(char* strOut, char* strIn)
{
    for ( ; *strIn; ++strIn) *strOut++ = tolower(*strIn);
}


/**
 Convert a string to upper

 @param strOut Output string pointer
 @param strIn Input string pointer
 */
void StringToUpper(char* strOut, char* strIn)
{
    for ( ; *strIn; ++strIn) *strOut++ = toupper(*strIn);
}


/**
 Write a disclaimer to an already opened file

 @param fil File pointer
 */
void writeDisclaimer(FILE *fil)
{
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    fprintf(fil,"%s", commentHeaderStart);
    fprintf(fil," ** Created by %s\r\n",strCreator);
    fprintf(fil," **\r\n");
    if (strCompany == NULL)
    {
        strCompany = strCreator;
    }
    fprintf(fil," ** Copyright © %d %s. All rights reserved.\r\n",tm.tm_year + 1900,strCompany);
    fprintf(fil," **\r\n");
    fprintf(fil,"%s\r\n",strDisclaimer);
    fprintf(fil,"%s",commentHeaderEnd);
}


/**
 Write a history to an already opened file

 @param fil File pointer
 */
void writeHistory(FILE *fil)
{
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    fprintf(fil,"%s", commentHeaderStart);
    fprintf(fil," **\\file %s\r\n",filename_c);
    fprintf(fil," **\r\n");
    fprintf(fil," ** %s\r\n",strModuleDescription);
    fprintf(fil," ** A detailed description is available at\r\n");
    fprintf(fil," ** @link %sGroup file description @endlink\r\n",strModuleName);
    fprintf(fil," **\r\n");
    fprintf(fil," ** History:\r\n");
    fprintf(fil," ** - %d-%d-%d  1.00  %s\r\n",tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday,strCreator);
    fprintf(fil,"%s",commentHeaderEnd);
}


/**
 Printout help
 */
void printHelp(void)
{
    printf("usage:\n");
    printf("%s -c Joe -m MyModule -d \"This is my module\"\n",appname);
    printf("\n");
    printf("-c name\n");
    printf("   name = Name of creator\n");
    printf("\n");
    printf("-m modulename\n");
    printf("   modulename = Name of module without special characters in CamelCase\n");
    printf("\n");
    printf("-d description\n");
    printf("   description = Description\n");
    printf("\n");
    printf("[-o]\n");
    printf("   optional company / organisation\n");
    printf("\n");
    printf("[-cpp]\n");
    printf("   optional geerate cpp extension\n");
}


/**
 Generate date

 @param pStringOut String to write the date into
 */
void generateDate(char* pStringOut)
{
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    sprintf(pStringOut,"%d-%d-%d",tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday);
}


/**
 Main function

 @param argc <#argc description#>
 @param argv <#argv description#>
 @return <#return value description#>
 */
int main(int argc, const char * argv[]) {
    printf("Welcome\n"); 
    if (argc <= 1)
    {
        printHelp();
        return -1;
    }
    
    for(int i = 1; i < argc;i++)
    {
        if (strncmp(argv[i],"-cpp",4) == 0)
        {
            cppMode = true;
        } else if (strncmp(argv[i],"-c",2) == 0)
        {
            strCreator = (char*)argv[i + 1];
            i++;
        } else if (strncmp(argv[i],"-m",2) == 0)
        {
            strModuleName = (char*)argv[i + 1];
            i++;
        } else if (strncmp(argv[i],"-d",2) == 0)
        {
            strModuleDescription = (char*)argv[i + 1];
            i++;
        } else if (strncmp(argv[i],"-out",4) == 0)
        {
            strOut = (char*)argv[i + 1];
            i++;
        } else if (strncmp(argv[i],"-o",2) == 0)
        {
            strCompany = (char*)argv[i + 1];
            i++;
        } else if (strncmp(argv[i],"-p",2) == 0)
        {
            strProjectName = (char*)argv[i + 1];
            genProject = true;
            i++;
        } else if (strncmp(argv[i],"-w",2) == 0)
        {
            printf("Changing into Dir: %s\n",argv[i + 1]);
            chdir(argv[i + 1]);
            i++;
        } else if (strncmp(argv[i],"-txt2c",6) == 0)
        {
            strIn = (char*)argv[i + 1];
            txt2c = true;
            i++;
        } else if (strncmp(argv[i],"-bin2c",6) == 0)
        {
            strIn = (char*)argv[i + 1];
            bin2c = true;
            i++;
        }
    }

    MALLOC_ZERO(projectname,100);
    MALLOC_ZERO(modulename,100);
    MALLOC_ZERO(MODULENAME,100);
    MALLOC_ZERO(filename_c,100);
    MALLOC_ZERO(filename_h,100);
    
    StringToLower(projectname,strProjectName);
    StringToLower(modulename,strModuleName);
    StringToUpper(MODULENAME,strModuleName);

    if (strcmp(MODULENAME,"MAIN") == 0)
    {
        isMain = true;
    }
    
    StringToLower(filename_c,strModuleName);
    if (cppMode)
    {
        strcat(filename_c,".cpp");
    }
    else
    {
        strcat(filename_c,".c");
    }
    StringToLower(filename_h,strModuleName);
    strcat(filename_h,".h");

    if (txt2c)
    {
        Txt2C(strIn,strOut);
        return 0;
    }

    if (bin2c)
    {
        Bin2C(strIn,strOut);
        return 0;
    }
    
    if (genProject)
    {
        char tmp[512] = {0}; 
        char strPathSource[512] = {0}; 
        char strPathVsCode[512] = {0};

        sprintf(strPathVsCode,"%s/.vscode",projectname);
        sprintf(strPathSource,"%s/src",projectname);

        if (stat(strPathVsCode, &st) == -1) {
            mkdir(strPathVsCode, 0777);
        }

        if (stat(projectname, &st) == -1) {
            mkdir(projectname, 0777);
        }

        WriteToFile(projectname,"CMakeLists.txt",strTemplateCmakeLists,projectname);
        WriteToFile(projectname,"build.sh",strBuildLinux);
        WriteToFile(projectname,"build.command",strBuildMac);
        WriteToFile(projectname,"build.bat",strBuildWindows);
        WriteToFile(projectname,"README.md",strReadme,projectname);
        WriteToFile(projectname,"DISCLAIMER.md",strDisclaimer);
        WriteToFile(strPathVsCode,"launch.json",strVSCodeLaunch,projectname,projectname,projectname);
        WriteToFile(strPathVsCode,"tasks.json",strVSCodeTasks);

        if (stat(strPathSource, &st) == -1) {
            mkdir(strPathSource, 0777);
        }
        //sprintf(tmp,"-c \"%s\" -m \"%s\" -d \"%s\" -o \"%s\"",strCreator,strModuleName,strModuleDescription,strCompany);
        sprintf(tmp,"%s -w \"%s\" -c \"%s\" -m \"%s\" -d \"%s\"",argv[0],strPathSource,strCreator,"Main","Main File");
        if (cppMode)
        {
            strcat(tmp," -cpp");
        }
        if (strCompany != NULL)
        {
            strcat(tmp," -o ");
            strcat(tmp,strCompany);
        }
        system(tmp); 
        return 0;
    }

    FILE *c_file = fopen(filename_c, "w");
    if (c_file == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }
    
    FILE *h_file = fopen(filename_h, "w");
    if (h_file == NULL)
    {
        printf("Error opening file!\n");
        exit(1);
    }
    
    //
    // Process C-File
    //
    writeDisclaimer(c_file);
    writeHistory(c_file);
    
    if (cppMode)
    {
        fprintf(c_file,"#define __%s_CPP__\r\n\r\n",MODULENAME);
    }
    else
    {
        fprintf(c_file,"#define __%s_C__\r\n\r\n",MODULENAME);
    }
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Include files\r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"\r\n");
    if (isMain)
    {
        fprintf(c_file,"#include <stdio.h>\r\n");
        fprintf(c_file,"#include <stdlib.h>\r\n");
    }
    fprintf(c_file,"#include <string.h> //required also for memset, memcpy, etc.\r\n");
    fprintf(c_file,"#include <stdint.h>\r\n");
    fprintf(c_file,"#include <stdbool.h>\r\n");
    //fprintf(c_file,"#include \"base_types.h\"\r\n");
    fprintf(c_file,"#include \"%s\"\r\n",filename_h);
    fprintf(c_file,"\r\n");
            
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Local pre-processor symbols/macros ('#define') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Global variable definitions (declared in header file with 'extern') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Local type definitions ('typedef') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Local variable definitions ('static') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Local function prototypes ('static') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** Function implementation - global ('extern') and local ('static') \r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"\r\n");
    
    if (isMain)
    {
        fprintf(c_file,"int main(int argc, const char * argv[])\r\n");
        fprintf(c_file,"{\r\n");
        fprintf(c_file,"    \r\n");
        fprintf(c_file,"    //add you initialization here...\r\n");
        fprintf(c_file,"    \r\n");
        fprintf(c_file,"    //main loop\r\n");
        fprintf(c_file,"    while(1)\r\n");
        fprintf(c_file,"    {\r\n");
        fprintf(c_file,"        //add your looping code here...\r\n");
        fprintf(c_file,"    }\r\n");
        fprintf(c_file,"}\r\n\r\n");
    } else
    {
        fprintf(c_file,"int %s_Init(stc_%s_handle_t* pstcHandle)\r\n",strModuleName,modulename);
        fprintf(c_file,"{\r\n");
        fprintf(c_file,"}\r\n\r\n");
                
        fprintf(c_file,"int %s_Deinit(stc_%s_handle_t* pstcHandle)\r\n",strModuleName,modulename);
        fprintf(c_file,"{\r\n");
        fprintf(c_file,"}\r\n\r\n");
    }
    fprintf(c_file,"\r\n");
    
    fprintf(c_file,"%s",commentHeaderStart);
    fprintf(c_file," ** EOF (not truncated)\r\n");
    fprintf(c_file,"%s",commentHeaderEnd);
    
    fclose(c_file);
    
    //
    // Process H-File
    //
    writeDisclaimer(h_file);
    writeHistory(h_file);
    
    fprintf(h_file,"#if !defined(__%s_H__)\r\n",MODULENAME);
    fprintf(h_file,"#define __%s_H__\r\n\r\n",MODULENAME);
    
    fprintf(h_file,"/* C binding of definitions if building with C++ compiler */\r\n");
    fprintf(h_file,"#ifdef __cplusplus\r\n");
    fprintf(h_file,"extern \"C\"\r\n");
    fprintf(h_file,"{\r\n");
    fprintf(h_file,"#endif\r\n\r\n");
    
    fprintf(h_file,"%s", commentHeaderStart);
    fprintf(h_file," ** \\defgroup %sGroup %s\r\n",strModuleName,strModuleDescription);
    fprintf(h_file," **\r\n");
    fprintf(h_file," ** Provided functions of %s:\r\n",strModuleName);
    fprintf(h_file," **\r\n");
    fprintf(h_file," **\r\n");
    fprintf(h_file,"%s", commentHeaderEnd);
    fprintf(h_file,"//@{\r\n\r\n");
    
    fprintf(h_file,"%s", commentHeaderStart);
    fprintf(h_file,"** \\page %s_module_includes Required includes in main application\r\n",modulename);
    fprintf(h_file,"** \\brief Following includes are required\r\n");
    fprintf(h_file,"** @code\r\n");
    fprintf(h_file,"** #include \"%s.h\"\r\n",modulename);
    fprintf(h_file,"** @endcode\r\n");
    fprintf(h_file,"**\r\n");
    fprintf(h_file,"%s", commentHeaderEnd);
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** (Global) Include files\r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    
    fprintf(c_file,"#include <stdint.h>\r\n");
    fprintf(c_file,"#include <stdbool.h>\r\n");
    fprintf(c_file,"\r\n");
    //fprintf(c_file,"#include \"base_types.h\"\r\n");
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** Global pre-processor symbols/macros ('#define') \r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** Global type definitions ('typedef') \r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    
    if (!isMain)
    {
        fprintf(h_file,"typedef struct stc_%s_handle\r\n",modulename);
        fprintf(h_file,"{\r\n");
        fprintf(h_file,"    uint8_t u8Dummy;\r\n");
        fprintf(h_file,"} stc_%s_handle_t;\r\n\r\n",modulename);
    }
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** Global variable declarations ('extern', definition in C source)\r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** Global function prototypes ('extern', definition in C source) \r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    fprintf(h_file,"\r\n");
    if (!isMain)
    {
        fprintf(h_file,"int %s_Init(stc_%s_handle_t* pstcHandle);\r\n",strModuleName,modulename);
        fprintf(h_file,"int %s_Deinit(stc_%s_handle_t* pstcHandle);\r\n",strModuleName,modulename);
        fprintf(h_file,"\r\n");
    }
    
    fprintf(h_file,"//@} // %sGroup\r\n\r\n",strModuleName);
    
    fprintf(h_file,"#ifdef __cplusplus\r\n");
    fprintf(h_file,"}\r\n");
    fprintf(h_file,"#endif\r\n\r\n");

    fprintf(h_file,"#endif /* __%s_H__ */\r\n\r\n",MODULENAME);
    
    fprintf(h_file,"%s",commentHeaderStart);
    fprintf(h_file," ** EOF (not truncated)\r\n");
    fprintf(h_file,"%s",commentHeaderEnd);
    
    fclose(h_file);

    return 0;
}
