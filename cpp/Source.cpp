//#include "proxy_model.cpp"
#include "Ensemble_opt.cpp"
#include "simulator.cpp"
#include <cstdlib> 
#include <fstream>
using namespace std;



void
read_from_file(const char * filename, dlib::matrix<double> &v){ //read a file as filename into a vector;
	double tmp;
	size_t n = 0;
	std::ifstream strm(filename);
	while (strm >> tmp)
	{
		n++;
	}
	v.set_size(n, 1);
	strm.close();
	strm.open(filename);
	for (unsigned i = 0; i < n; i++)
	{
		strm >> v(i, 0);
	}
}

void read_from_inputfile(string inputfilename, vector<vector<double>> &line){
	line.resize(6);
	ifstream inFile;
	double num;
	string stmp;
	const char* stmp1;
	inFile.open(inputfilename);
	while (!inFile.eof()){
		getline(inFile, stmp);
		//strcpy(stmp1, stmp.c_str());
		stmp1 = stmp.c_str();
		if (strcmp(stmp1, "***") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[0].push_back(num);
				inFile >> num;
			}
		}
		if (strcmp(stmp1, "****") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[1].push_back(num);
				inFile >> num;
			}
		}
		if (strcmp(stmp1, "*****") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[2].push_back(num);
				inFile >> num;
			}
		}
		if (strcmp(stmp1, "******") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[3].push_back(num);
				inFile >> num;
			}
		}
		if (strcmp(stmp1, "*******") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[4].push_back(num);
				inFile >> num;
			}
		}
		if (strcmp(stmp1, "********") == 0){
			inFile >> num;
			while (num != 0.00001){
				line[5].push_back(num);
				inFile >> num;
			}
		}
	}
}
void out_to_file(vector<vector<double>> &line){
	ofstream myfile;
	myfile.open("input_other.txt");
	myfile << line[0][0] << "\n";
	for (unsigned i = 1; i < line[0][0] + 1; i++){
		myfile << line[0][i] << "\n";
	}
	for (unsigned i = line[0][0] + 1; i < line[0][0] * 2 + 1; i++){
		myfile << line[0][i] << "\n";
	}
	int index = line[0][0] * 2 + 1;
	myfile << line[0][index] << "\n";
	for (unsigned i = index+1; i < line[0][0]+index + 1; i++){
		myfile << line[0][i] << "\n";
	}
	for (unsigned i = 0; i < 11; i++){
		myfile << line[1][i] << "\n";
	}
	myfile.close();
	////myfile.open("input/temp/initial.dat");
	////for (unsigned i = 0; i < line[0][0] * line[0][1] * 2 + line[0][0]; i++){
	////	myfile << line[2][i] << "\n";

	//}
	//myfile.close();
	myfile.open("input.txt");
	for (unsigned i = 0; i < line[0][0] * line[0][1] * 2 + line[0][0]; i++){
		myfile << line[2][i] << "\n";

	}
	myfile.close();
	myfile.open("input/temp/economic.dat");
	myfile << line[3][0] << "\n";
	myfile << line[3][1] << "\n";
	myfile << line[3][2] << "\n";
	myfile << line[3][3] << "\n";
	myfile.close();
	myfile.open("input/temp/parameter.dat");
	myfile << line[4][0] << "\n";
	myfile << line[4][1] << "\n";
	myfile << line[4][2] << "\n";
	myfile << line[4][3] << "\n";
	myfile << line[4][4] << "\n";
	myfile << line[4][5] << "\n";
	myfile.close();
	myfile.open("input/temp/iteration.dat");
	myfile << line[5][0] << "\n";
	myfile << line[5][1] << "\n";
	myfile.close();
	myfile.open("input/temp/varia-numb.dat");
	myfile << line[2].size() << "\n";
	myfile.close();
	myfile.open("input/temp/well-stage-numb.dat");
	myfile << line[0][0] << "\n";
	myfile << line[0][1] << "\n";
	myfile.close();
}

	int main()
{ 
	vector<vector<double>> line;
	read_from_inputfile("input/inputfile.dat", line);
	//std::cout << " line =" << line[3][0];
	out_to_file(line);
	double NPV;
	//system("CMG\\run7.bat");
	//system("run7.bat");
	dlib::matrix<double> x;
	read_from_file("input/temp/initial.dat", x);
	/*En_optimization<simulator> stosag(15, "GBR");*/
	En_optimization<simulator> stosag(15);
	stosag.optimize_0_1_scale(x);
	//simulator reservoir_sim(15);
	//reservoir_sim.run(x,NPV);
	//std::cout << x << std::endl;
	//std::cout <<"NPV is :"<< NPV << std::endl;

	//ofstream myfile;
	//myfile.open("sim_NPV.dat");
	//myfile << NPV << std::endl;
	//myfile.close();
}