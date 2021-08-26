#include <iostream>
#include <string.h>
#include <cmath>
#include <chrono>
#include <numeric>
#include <thread>
#include <vector>
#include <bits/stdc++.h>

using namespace std;

void reverseArray(int arr[], int n);
void int_to_bin_digit(unsigned int in, int count, int* out);
int bin_digit_to_int(int* number, int size);
void print_bin_arr(int* arr, int n);
void print_in_bin(int num);
void print_differences(int exponent, int* predictions);

int power(long long x, unsigned int y, int p);
int exponentation(int base, int exponent, int mod, int* timestamps);

void set_up_predictions(int* times, int* predictions, int* avg_diff, int avg, int s);
int get_next_bit_index(int* diffs, int s);
int brute_force(int* number,int len, vector<int>indexes, int base, int mod, int res);


int main(){
  int g = 23;
  int a = 1622656324;
  int m = 1623464321;

  //bitlength of exponent
  int s = ceil(log2((double)a));

  //create an array to store execution times
  int times[s];
  times[s-1] = 1;

  int predictions[s];
  int avg_diff[s];

  int result = exponentation(g, a, m, times);

  //calculate avg multiplication time
  //skip first runs - cache is setting up, unreliable results
  int avg = 0;
  avg  = accumulate(times, times+(s-3), avg);
  avg /= s-2;
  cout <<"avg" << avg << endl;

  set_up_predictions(times, predictions, avg_diff, avg, s);

  //print time diff from avg for each index
  for(int i=0; i<s; i++){
    cout << i << " : " << avg_diff[i] << endl;
  }

  print_differences(a, predictions);

  print_in_bin(a);
  reverseArray(predictions, s); //required for brute force - index 0 - highest bit
  print_bin_arr(predictions, s);

  //indexes to check in brute force algorithm
  vector<int> indexes;
  indexes.push_back(1);
  indexes.push_back(2);

  int brute_force_res = brute_force(predictions, s, indexes, g, m, result);
  int new_index;
  while ( brute_force_res != a ){
    new_index = get_next_bit_index(avg_diff, s);
    if(new_index == -1){
      continue;
    }

    cout << "new index to check: " <<     new_index << endl;
    indexes.push_back(s-new_index-1);
    brute_force_res = brute_force(predictions,s,indexes,g,m,result);
  }

  cout << "exponent found: " << brute_force_res << endl;
  string info = ((brute_force_res == a) == 1) ? "YES" : "NO";
  cout << "correct? : " << info << endl;

  return 0;
}

int brute_force(int* number,int len, vector<int>indexes, int base, int mod,int res){
  if(indexes.size() == 0){
    return -1;
  }

  int curr_index = indexes.back();
  indexes.pop_back();

  number[curr_index]=(number[curr_index]==0) ? 1 : 0;

  int exponent = bin_digit_to_int(number,len);
  if( power(base, exponent, mod) == res){
    return exponent;
  }
  exponent = brute_force(number,len,indexes, base,mod,res);
  if(exponent != -1){
    return exponent;
  }

  number[curr_index]=(number[curr_index]==0) ? 1 : 0;
  exponent = bin_digit_to_int(number,len);

  if(power(base,exponent, mod)==res){
    return exponent;
  }

  return brute_force(number,len,indexes, base,mod,res);
}

void set_up_predictions(int* times, int* predictions, int* avg_diff, int avg, int s){
  predictions[s-1] = 1;
  predictions[s-2] = 1;
  predictions[s-3] = 1;

  avg_diff[s-1]=INT_MAX;
  avg_diff[s-2]=INT_MAX;
  avg_diff[s-3]=INT_MAX;

  for(int i=s-4; i>=0; i--){
    if(times[i] > avg){
      predictions[i] = 1;
    }else{
      predictions[i] = 0;
    }
    avg_diff[i] = abs(times[i] - avg);
    //an exceptionally large difference is also suspicious ->
    //we set it to negative value to be taken into account in the "get_next_bit_index" function
    if(avg_diff[i] > 1.5 * avg){
      avg_diff[i] = -1;
    }
  }
}

void print_bin_arr(int* arr, int n){
  for(int i=0;i<n;i++){
    cout << arr[i];
  }
  cout << endl;
}

void print_in_bin(int num){
  int s = ceil(log2((double)num));
  for(int i=0; i<s; i++){
    cout<< ((num>>s-i-1) & 1);
  }
  cout << endl;
}

int get_next_bit_index(int* diffs, int s){
  int tmp = INT_MAX;
  int index = -1;
  for(int i=0; i<s; i++){
    if(diffs[i] < tmp){
      tmp = diffs[i];
      index = i;
    }
  }
  diffs[index] = INT_MAX;
  return index;
}
void reverseArray(int* arr, int n){
   for (int low = 0, high = n - 1; low < high; low++, high--){
      swap(arr[low], arr[high]);
   }
}
int exponentation(int base, int exponent, int mod, int* timestamps){
  int size = ceil(log2((double)exponent));
  long y = base;
  short curr_bit;
  for(int i=size-2; i>=0; i--){
    curr_bit = ((exponent >> i) & 1);
    auto start = chrono::steady_clock::now();
    if(curr_bit == 0){
        y = (y * y) % mod ;
    }else{
      y = ((y * y % mod ) * base) % mod;
    }

    auto end = chrono::steady_clock::now();
    timestamps[i] = (int)chrono::duration_cast<chrono::nanoseconds>(end - start).count();
  }

  return y;
}
int power(long long x, unsigned int y, int p){
    int res = 1;x = x % p;if (x == 0) return 0;while (y > 0) {    if (y & 1)  res = (res*x) % p; y = y>>1;x = (x*x) % p; } return res;
}
void int_to_bin_digit(unsigned int in, int count, int* out)
{
    /* assert: count <= sizeof(int)*CHAR_BIT */
    unsigned int mask = 1U << (count-1);
    int i;
    for (i = 0; i < count; i++) {
        out[i] = (in & mask) ? 1 : 0;
        in <<= 1;
    }
}

int bin_digit_to_int(int* number, int size){
  int res = 0;
  for(int i=0; i<size; i++){
    if(number[i]==1){
      res += pow(2.0,size-i-1);
    }
  }
  return res;
}


void print_differences(int exponent, int* predictions){
  int s = ceil(log2((double)exponent));

  cout << "Original exponent and predicted differs at index: ";
  for(int i=0;i<s;i++){
      if(predictions[s-i-1] != ((exponent>>s-i-1) & 1)){
        cout << s-i-1 << " ";
      }
  }
  cout << endl;
}
