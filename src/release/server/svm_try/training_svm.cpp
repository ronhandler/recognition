#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cvaux.h>

#include <iostream>
#include <vector>

using namespace std;
using namespace cv;

int main ( int argc, char** argv )
{
    cout << "OpenCV Training SVM Automatic Stolen From The Net\n";
    cout << "\n";

    char* path_Plates;
    char* path_NoPlates;
    int numPlates;
    int numNoPlates;
    int imageWidth=320;
    int imageHeight=240;

    //Check if user specify image to process
    if(argc >= 5 )
    {
        numPlates= atoi(argv[1]);
        numNoPlates= atoi(argv[2]);
        path_Plates= argv[3];
        path_NoPlates= argv[4];

    }else{
        cout << "Usage:\n" << argv[0] << " <num Plate Files> <num Non Plate Files> <path to plate folder files> <path to non plate files> \n";
        return 0;
    }        

    Mat classes;//(numPlates+numNoPlates, 1, CV_32FC1);
    Mat trainingData;//(numPlates+numNoPlates, imageWidth*imageHeight, CV_32FC1 );

    Mat trainingImages;
    vector<int> trainingLabels;

    for(int i=0; i< numPlates; i++)
    {

        stringstream ss(stringstream::in | stringstream::out);
        ss << path_Plates << i << ".jpg";
        cout << ss;
        cout << ss.str() << endl;
        Mat img=imread(ss.str(), 0);
        //Mat img2;
        //cvtColor(img, img2, CV_BGR2GRAY);
        //img2= img2.reshape(1, 1);
        trainingImages.push_back(img);
        trainingLabels.push_back(1);
    }

    for(int i=0; i< numNoPlates; i++)
    {
        stringstream ss(stringstream::in | stringstream::out);
        ss << path_NoPlates << i << ".jpg";
        Mat img=imread(ss.str(), 0);
        //Mat img2;
        //cvtColor(img, img2, CV_BGR2GRAY);
        //img2= img2.reshape(1, 1);
        trainingImages.push_back(img);
        trainingLabels.push_back(0);

    }

    Mat(trainingImages).copyTo(trainingData);
    //trainingData = trainingData.reshape(1,trainingData.rows);
    trainingData.convertTo(trainingData, CV_32FC1);
    Mat(trainingLabels).copyTo(classes);

    FileStorage fs("SVM.xml", FileStorage::WRITE);
    fs << "TrainingData" << trainingData;
    fs << "classes" << classes;
    fs.release();

    return 0;
}
