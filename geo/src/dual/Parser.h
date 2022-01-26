#ifndef PARSER_H
#define PARSER_H


#include <string>
#include <fstream>
#include <map>
#include <vector>

class Parser
{
public:
    Parser()
    {
        initialize();
        ymlFile = "";
    };
    Parser(std::string yfile);

    void file(std::string yfile)
    {
        ymlFile=yfile;
    };
    void templateFile();
    void read();
    std::string stringVal(std::string key);
    bool boolVal(std::string key);
    double doubleVal(std::string key);
    std::tuple<double,double,double> lowerVal(std::string key);
    std::tuple<double,double,double> upperVal(std::string key);
private:
    void initialize();
    void splitAssign(std::string s);
    std::vector<std::string> splitByCommaIgnore(std::string s);
    void removeWhiteSpaceAndComments(std::string &s);
    std::string ymlFile;
    std::map<std::string, std::string> inputs;

};


#endif



