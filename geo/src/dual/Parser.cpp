#include "Parser.h"

#include<iostream>
#include <algorithm>
#include <cctype>
#include <string>



Parser::Parser(std::string yfile)
{
    ymlFile=yfile;
    initialize();

}

void Parser::initialize()
{
    inputs["version:"]="1.1";
    inputs["boundary_refine:"]="true";
    inputs["developer_output:"]="true";
    inputs["boundary:"]="filename.txt # space delimited xy-pairs, 1 line for each ";
    inputs["bounding_box:"]= "{(0,0),(0, 0)} # equal points or left off will default to tight bounding box"; //"{(lower_x,lower_y),(upper_x, upper_y)}";
    inputs["resolution:"] = "0.5";
    inputs["output_file:"] = "mesh  # extension will be added automatically" ;

}
void Parser::read()
{
    if(ymlFile!="")
    {
        std::ifstream in_file(ymlFile.c_str());
        std::string tmp;
        std::getline(in_file,tmp);
        while(!in_file.eof()&&!in_file.fail())
        {
            splitAssign(tmp);
            std::getline(in_file,tmp);
        }
        in_file.close();
    }
}

void Parser::templateFile()
{
    std::ofstream out_file("example.yml");

    for( std::map<std::string, std::string>::iterator it = inputs.begin(); it!=inputs.end(); ++it)
    {
        out_file<<it->first<<it->second<<std::endl;
    }
    out_file.close();
}
void Parser::splitAssign(std::string s)
{
    std::string key="";
    std::string val="";
    bool val_record = false;

    if(s.length()>1 && s[0]=='#')
        return;
    for(unsigned int lcv = 0; lcv < s.length(); ++lcv)
    {
        if(s[lcv]=='#')
            break;
        if(val_record)
            val = val+s[lcv];
        else
            key = key+s[lcv];

        if(s[lcv]==':')
            val_record = true;


    }
    if(val_record)
    {
        inputs[key]=val;
        //std::cout<<"Key: "<<key<<" value: "<<val<<std::endl;
    }
}
std::string Parser::stringVal(std::string key)
{
    if(inputs.find(key)!=inputs.end())
        return inputs[key];
    else
        return "";
}
double Parser::doubleVal(std::string key)
{
    if(inputs.find(key)!=inputs.end())
        return atof(inputs[key].c_str());
    else
        return 0;
}
bool Parser::boolVal(std::string key)
{

    if(inputs.find(key)!=inputs.end())
    {
        std::string val =inputs[key];
        std::transform(val.begin(), val.end(), val.begin(),[](unsigned char c)
        {
            return std::tolower(c);
        });
        if(val=="true" || val == "1" || val == "t")
            return true;
        else
            return false;
    }
    else
        return false;

}
std::tuple<double,double,double> Parser::lowerVal(std::string key)
{
    std::vector<std::string> vals;
    if(inputs.find(key)!=inputs.end())
    {
        //{(lower_x,lower_y),(upper_x, upper_y)}
        vals = splitByCommaIgnore(inputs[key]);
        if(vals.size()==6) ///3D specification
        {
            return std::tuple<double,double,double> (std::atof(vals[0].c_str()),std::atof(vals[1].c_str()),std::atof(vals[2].c_str()));
        }
        else if(vals.size()==4) ///2D specification
        {
            return std::tuple<double,double,double> (std::atof(vals[0].c_str()),std::atof(vals[1].c_str()),0);
        }
    }
    return std::tuple<double,double,double> (0,0,0);
}
std::tuple<double,double,double> Parser::upperVal(std::string key)
{
    std::vector<std::string> vals;
    if(inputs.find(key)!=inputs.end())
    {
        //{(lower_x,lower_y),(upper_x, upper_y)}
        vals = splitByCommaIgnore(inputs[key]);
        if(vals.size()==6) ///3D specification
        {
            return std::tuple<double,double,double> (std::atof(vals[3].c_str()),std::atof(vals[4].c_str()),std::atof(vals[5].c_str()));
        }
        else if(vals.size()==4) ///2D specification
        {
            return std::tuple<double,double,double> (std::atof(vals[2].c_str()),std::atof(vals[3].c_str()),0);
        }
    }
    return std::tuple<double,double,double> (0,0,0);

}
std::vector<std::string> Parser::splitByCommaIgnore(std::string s)
{
    std::vector<std::string> vals;
    std::string tmp = "";
    for(unsigned int lcv = 0; lcv < s.length(); ++lcv)
    {
        if(s[lcv]==',')
        {
            vals.push_back(tmp);
            tmp = "";
        }
        else if(s[lcv]!= '(' && s[lcv]!= '{' && s[lcv]!= ')' && s[lcv]!= '}'&& s[lcv]!= ']'&& s[lcv]!= '[')
            tmp=tmp+s[lcv];

    }
    vals.push_back(tmp);
    return vals;
}
