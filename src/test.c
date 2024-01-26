#include <check.h>
#include <stdio.h>

#include "a.c"
#include "a.h"
#include "calc.c"

START_TEST(simple) {
  ck_assert_double_eq(not_main("2+2="), 4);
  ck_assert_double_eq(not_main("2*2="), 4);
  ck_assert_double_eq(not_main("2/2="), 1);
  ck_assert_double_eq(not_main("2-2="), 0);
  ck_assert_double_eq(not_main("6/5="), 1.2);
  ck_assert_double_eq(not_main("2^2="), 4);
  ck_assert_double_eq(not_main("5mod2="), 2);
  ck_assert_double_eq(not_main("sqrt(4)="), 2);
  ck_assert_double_eq(not_main("2+2*2="), 6);
  ck_assert_double_eq(not_main("-5-5="), -10);
  ck_assert_double_eq(not_main("5--5="), 10);
  ck_assert_double_eq(not_main("5*(3+2)="), 25);
  ck_assert_double_eq(
      not_main("1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+"
               "1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+"
               "1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+"
               "1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1="),
      109);
}
END_TEST

START_TEST(simple_trig) {
  ck_assert_double_eq_tol(not_main("ln(10)="), 2.30258509, 1e-7);
  ck_assert_double_eq_tol(not_main("acos(0.5)="), 1.0471976, 1e-7);
  ck_assert_double_eq_tol(not_main("sin(1)="), 0.84147098, 1e-7);
  ck_assert_double_eq_tol(not_main("tan(1)="), 1.5574077, 1e-7);
  ck_assert_double_eq_tol(not_main("cos(1)="), 0.54030231, 1e-7);
  ck_assert_double_eq_tol(not_main("log(5)="), 0.698970004, 1e-7);
  ck_assert_double_eq_tol(not_main("asin(1)="), 1.5707963, 1e-7);
  ck_assert_double_eq_tol(not_main("atan(1)="), 0.7853982, 1e-7);

  // ck_assert_double_eq(not_main("ln(10)="), 0);
}
END_TEST

START_TEST(credit) {
  ck_assert_double_eq_tol(credit_d("1000000", "2", "6", "13"), 1167916.67,
                          1e-2);

  ck_assert_double_eq_tol(credit_a("1000000", "2", "6", "13"), 39221.55, 1e-2);
}
END_TEST

START_TEST(vklad) {
  int days[1], nalog[1], new_year[1];
  days[0] = 31;
  nalog[0] = 364;
  new_year[0] = 365;
  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 1, 1),
      19958.9, 10);
  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 2, 1),
      0, 10);
  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 3, 1),
      5019958.90, 10);

  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 1, 2),
      19958.9, 1e-2);
  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 2, 2),
      0, 1e-2);
  ck_assert_double_eq_tol(
      vklad_not("5000000", 31, "4.7", "", days, nalog, 1, "13", new_year, 3, 2),
      5000000, 1e-2);
  days[0] = 365;
  int new_year_2[2], nalog_2[2];
  new_year_2[0] = 365;
  new_year_2[1] = 366;
  nalog_2[0] = 364;
  nalog_2[1] = 730;
  ck_assert_double_eq_tol(vklad_not("500000000", 365, "4.7", "", days, nalog_2,
                                    1, "13", new_year_2, 1, 1),
                          23499824.09, 1e-2);
  ck_assert_double_eq_tol(vklad_not("500000000", 365, "4.7", "", days, nalog_2,
                                    1, "13", new_year_2, 2, 1),
                          3039377.13, 1e-2);
  ck_assert_double_eq_tol(vklad_not("500000000", 365, "4.7", "", days, nalog_2,
                                    1, "13", new_year_2, 3, 1),
                          523499824.09, 1e-2);

  int day_2[2];
  day_2[0] = 31;
  day_2[1] = 59;
  ck_assert_double_eq_tol(vklad_not("5000000", 59, "4.7", "31 50000", day_2,
                                    nalog, 1, "13", new_year, 1, 1),
                          38238.53, 1e-2);
  ck_assert_double_eq_tol(vklad_not("5000000", 59, "4.7", "31 50000", day_2,
                                    nalog, 1, "13", new_year, 2, 1),
                          0, 1e-2);
  ck_assert_double_eq_tol(vklad_not("5000000", 59, "4.7", "31 50000", day_2,
                                    nalog, 1, "13", new_year, 3, 1),
                          5088238.53, 1e-2);
}
END_TEST

Suite *test_suite(void) {
  Suite *s;
  TCase *tc_core;

  s = suite_create("Parsers");

  tc_core = tcase_create("Core");

  tcase_add_test(tc_core, simple);
  tcase_add_test(tc_core, simple_trig);
  tcase_add_test(tc_core, credit);
  tcase_add_test(tc_core, vklad);

  suite_add_tcase(s, tc_core);

  return s;
}

int main(void) {
  int number_failed;
  Suite *s;
  SRunner *sr;

  s = test_suite();
  sr = srunner_create(s);

  srunner_run_all(sr, CK_NORMAL);
  number_failed = srunner_ntests_failed(sr);
  srunner_free(sr);

  return (number_failed == 0) ? 0 : 1;
}