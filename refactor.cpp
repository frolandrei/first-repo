#include <iostream>
#include <vector>

double bestMod(double a)
{
  if (a >= 0) {
    return a; 
      } else {
            double b=a-(2*a);
            return b;
  }
}

int main()
{
  std::vector<double> test_cases = {-1.0, -0.5, 0.0, 0.5, 1.0};
  int xyzw=0;
  while (xyzw < test_cases.size()) {
      if (bestMod(test_cases[xyzw]) != abs(test_cases[xyzw])) {
        std::cout << "Тест не пройден " << test_cases[xyzw] << "   ";
      } else { 
        std::cout << bestMod(test_cases[xyzw]) << "  ";
    }
    xyzw=xyzw+1;
}
}
