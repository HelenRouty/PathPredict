#include <iostream>
#include <cmath>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <stdlib.h>

using namespace std;

double mean(vector<double> arr){
    int n = arr.size();
    double sum = 0;
    for(int i = 0; i < n; i++){
        sum += arr[i];
    }
    
    return sum/n;
}

double upper(vector<double> arr, vector<double> brr){
    double arr_mean = mean(arr);
    double brr_mean = mean(brr);
    int n = arr.size();
    double sum = 0;
    for (int i = 0; i < n; i++) {
        double diff_ai = arr[i] - arr_mean; // xi - xmean
        double diff_bi = brr[i] - brr_mean; // yi - ymean
        sum += (diff_ai * diff_bi);
    }
    return sum;
}

double lower1 (vector<double> arr){
    double sum = 0;
    int n = arr.size();
    double arr_mean = mean(arr);
    for(int i = 0; i < arr.size(); i++){
        double diff = arr[i] - arr_mean;
        sum += (diff * diff);
    }
    
    return sqrt(sum);
}

double corr (vector<double> arr, vector<double> brr){
    double l1 = lower1(arr);
    double l2 = lower1(brr);
    if(!l2 || !l1) return 0;
    return upper(arr, brr)/(l1*l2);
}




int main(int argc, char* argv []){
    
    string list1 = argv[1];
    string list2 = argv[2];
    string output_filename = list1.substr(0, 1)
                            + list2.substr(0, 1) + ".txt";
    ifstream file1(list1);
    string line1;
    
    
    while(getline(file1, line1)){
        istringstream iss(line1);
        vector<string> tokens1;
        copy(istream_iterator<string>(iss),
             istream_iterator<string>(),
             back_inserter(tokens1));
        string id1 = tokens1[0];
        vector<double> v1;
        for(int i = 1; i < tokens1.size(); i ++){
            double tmp = atof(tokens1[i].c_str());
            v1.push_back(tmp);
        }
        
        
        ifstream file2(list2);
        string line2;
        
        while(getline(file2, line2)){
            istringstream iss2(line2);
            vector<string> tokens2;
            copy(istream_iterator<string>(iss2),
                 istream_iterator<string>(),
                 back_inserter(tokens2));
            string id2 = tokens2[0];
            vector<double> v2;
            for (int i = 1; i < tokens2.size(); i++) {
                double tmp = atof(tokens2[i].c_str());
                v2.push_back(tmp);
            }
            ofstream outfile;
            outfile.open(output_filename, std::ios_base::app); // change to output_filename
            outfile << id1 << " " << id2 << " " << corr(v1, v2) << endl;
            
            cout << id1 << " " << id2 << " " << corr(v1, v2) << endl;
            
        } // end inner while
    }// end outer while
    
    
    
    
//    vector<double> arr;
//    arr.push_back(1);
//    arr.push_back(2);
//    arr.push_back(3);
//
//    vector<double> brr;
//    brr.push_back(1);
//    brr.push_back(2);
//    brr.push_back(3);
//
//
//    double myCorr = corr(arr, brr);
//    cout << "mean " << mean(arr) << endl;
//    cout << "upper " << upper(arr, brr) << endl;
//    cout << "lower1 " << lower1(arr) << endl;
//    
//    cout << myCorr << endl;
    
    

}


