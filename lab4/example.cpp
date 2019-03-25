#include <iostream>
#include <fstream>
#include <list>
#include <cmath>
#include <string>
#include <cstring>

using namespace std;
typedef char string100[100];


class Query {
  private:
    string description;
    float value;
  public:
    Query(){}

    void setDescription(string d){
      description = d;
    }

    void setValue(float v){
      value = v;
    }

    string getDescription(){
      return description;
    }

    float getValue(){
      return value;
    }
};

class Probability {

  private:
     string description;
     float value;


  public:
    Probability(){}

    string getDescription(){
      return description;
    }

    float getValue(){
      return value;
    }

    void setDescription(string d){
      description = d;
    }

    void setValue(float v){
      value = v;
    }
};



class Main {
  private:
    list<Query> queries;
    list<Probability> probabilites;

  public:
    Main(){probabilites.begin(),queries.begin();}

    list<Probability> getProbabilites(){
      return probabilites;
    }

    list<Query> getQueries(){
      return queries;
    }

    /*
    * Parses the input given (see folder Tests with input examples)
    */
    void parse(){
      int numberOfProbabilities, numberOfQueries, pos;

      ifstream infile;
    	infile.open ("../Tests/Sprinkler,Rain,GrassWet.txt");
      string line;

      getline(infile, line);
      infile >> numberOfProbabilities;
      cout << numberOfProbabilities<<endl;
      string up_probabilities[numberOfProbabilities];
      Probability aux_probabilities;

      for (int i=0; i<numberOfProbabilities; i++) {
        getline(infile, line);
        infile >> up_probabilities[i];
        pos = up_probabilities[i].find("=");

        aux_probabilities.setDescription(up_probabilities[i].substr(0, pos));
        aux_probabilities.setValue(stof(up_probabilities[i].substr(pos+1)));
        probabilites.push_back(aux_probabilities);
      }

      getline(infile, line);
      infile >> numberOfQueries;
      cout << numberOfQueries<<endl;
      string up_queries[numberOfQueries];
      Query aux_queries;

      for (int i=0; i<numberOfQueries; i++) {
        getline(infile, line);
        infile >> up_queries[i];
        aux_queries.setDescription(up_queries[i]);
        queries.push_back(aux_queries);
      }
    	infile.close();
  }

  void fill_table(){
    list<Probability> probabilites_copy = probabilites;
    Probability aux_probabilities;
    string description;
    float value;


    for (auto v : probabilites_copy){
        description = v.getDescription();
        value = 1.0 - v.getValue();
        aux_probabilities.setValue(value);
        description.at(0)=(v.getDescription().at(0)=='+')?'-':'+';
        aux_probabilities.setDescription(description);
        probabilites.push_back(aux_probabilities);
    }
  }

  /**
   * Enumerates the probabilities according to the Bayes network algorithm
   * @param String Array probabilities
   */
  void enumerate(string *probabilities, int probabilities_size){
     int length = (int) pow(2, probabilities_size);
     string100 **new_probabilities;// [length][probabilities_size];
     new_probabilities = (string100**) malloc (length*sizeof(string100*));
     for (int i = 0; i<length; i++) {
       new_probabilities[i] = (string100*) malloc (probabilities_size*sizeof(string100));
     }
    int start = 0;
    int mid = (start+(length-start))/2;

    halfTrueHalfFalse(probabilities, probabilities_size, "+", 0, mid, 0, new_probabilities);
    halfTrueHalfFalse(probabilities, probabilities_size, "-", mid, length, 0, new_probabilities);

  //  printMatrix(new_probabilities, length, probabilities_size);

    for (int i=0; i<length; i++) {
      free(new_probabilities[i]);
    }
    free(new_probabilities);
  }

  /**
   * Prints the given matrix
   * @param String[][] matrix
   */

  void printMatrix (string100 **matrix, int matrix_size, int matrix0_size) {
    int i, j;

    for (i = 0; i< matrix_size; i++) {
      for (j = 0; j < matrix0_size; j++) {
        cout<<matrix[i][j];
      }
      cout<<endl;
    }
  }

  /**
   * Fills the 2D array new probabilities with all possible combinations of signs among the elements of the prob array
   * @param String Array prob, String sign, int start, int end, int element, String 2D array new_probabilities
   */
  void halfTrueHalfFalse(string *prob, int prob_size, string sign, int start, int end, int element, string100 **new_probabilities){
    if(element < prob_size){ //validation
      for (int i = start; i < end; i++){
        strcpy(new_probabilities[i][element], (sign + prob[element]).c_str());
      }
      //recursive calls
      int mid = start + ((end-start)/2);
        halfTrueHalfFalse(prob, prob_size, "+", start, mid, element+1, new_probabilities);
        halfTrueHalfFalse(prob, prob_size, "-", mid, end, element+1, new_probabilities);
    }
  }
 };





int main ()
{
  Main p;
  p.parse();
  p.fill_table();
  for (auto v : p.getProbabilites()){
    cout<<v.getDescription()<<" "<<v.getValue()<<endl;
  }
  string probabilities[]={"Sprinkler", "Rain", "GrassWet", "a", "b"};
  int probabilities_size = sizeof(probabilities)/sizeof(probabilities[0]);
  cout<<probabilities_size<<endl;
  p.enumerate(probabilities, probabilities_size);
  return 0;
}