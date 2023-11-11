double myBestFunctionToFindModuleOfADoubleNumber(double a)
{
  if (a > 0)
    return a
  return -a;
}

int main()
{
  std::vector test_cases = -1.0, -0.5, 0.0, 0.5, 1.0;
  for (auto test_case : test_cases)
    {
      if (myBestFunctionToFindModuleOfADoubleNumber(test_case) != abs(test_case))
        std::cout << "Тест не пройден " << test_case << std::endl;
    }
}
