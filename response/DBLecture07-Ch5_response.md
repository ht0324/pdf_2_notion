## 다른 프로그래밍 언어에서 SQL 사용하기

- 일반 프로그래밍 언어(C/C++/Java 등)와 함께 SQL을 사용해야 하는 이유:
  - 모든 쿼리를 SQL로 표현할 수 없음
    - 일부 쿼리는 일반 프로그래밍 언어로 더 쉽게 작성 가능
  - SQL에서는 선언적이지 않은 작업을 수행할 수 없음
    - 예: 보고서 출력, 사용자와의 상호 작용, 쿼리 결과를 GUI로 전송

## JDBC와 ODBC

- **JDBC와 ODBC**
  - 프로그램이 데이터베이스 서버와 상호 작용하기 위한 API
  - 애플리케이션에서 다음 작업을 위해 호출:
    - 데이터베이스 서버에 연결
    - SQL 쿼리를 데이터베이스 서버로 전송
    - 결과 튜플을 하나씩 프로그램 변수로 가져오기
- **ODBC (Open Database Connectivity)**
  - C, C++, C#, Visual Basic에서 작동
- **JDBC (Java Database Connectivity)**
  - Java에서 작동

## JDBC

- JDBC는 SQL용 Java API
- 데이터베이스와 통신하는 모델:
  1. 연결 열기
  2. "Statement" 객체 생성
  3. "Statement" 객체를 사용하여 쿼리 실행, 쿼리 전송 및 결과 가져오기
  4. 오류 처리를 위한 예외 메커니즘

## Public static void JDBCexample(String dbid, String userid, String passwd)

```java
try {
    Connection conn = DriverManager.getConnection(
        "jdbc:postgresql://localhost/db_name",
        userid, passwd);
    Statement stmt = conn.createStatement();
    /* 실제 작업 수행 ... 다음 슬라이드에 표시 */
    stmt.close();
    conn.close();
} catch (SQLException sqle) {
    System.out.println("SQLException : " + sqle);
}
```

psql 비밀번호를 변경하려면 psql에서 다음 stmt를 실행하세요:
ALTER USER your_userid WITH PASSWORD 'your_password';

## JDBC 코드 (계속)

### 데이터베이스 업데이트

```java
try {
    stmt.executeUpdate(
        "insert into instructor values ( '77987', 'Kim', 'Physics', 98000)");
} catch (SQLException sqle) {
    System.out.println("Could not insert tuple. " + sqle);
}
```

### 쿼리 실행, 결과 가져오기 및 출력

```java
ResultSet rset = stmt.executeQuery(
    "select dept_name, avg (salary) " +
    "from instructor " +
    "group by dept_name");
while (rset.next()) {
    System.out.println(rset.getString("dept_name") + 
                       " " + rset.getFloat(2));
}
```

## JDBC 코드 세부 사항

- **결과 필드 가져오기:**
  - `dept_name`이 `select`의 첫 번째 인수인 경우 `rset.getString("dept_name")`과 `rset.getString(1)`은 동일
- **Null 값 처리**
  - `if (rset.wasNull())`
    - `Systems.out.println("Got null value");`
- **경고: Statement는 안전하지 않음**
  - **경고:**
    - 입력으로 받은 문자열을 연결하여 쿼리를 생성하지 마세요
    - 예: `stmt.executeUpdate("SELECT dept_name FROM students " + "WHERE name = '" + name + "' ");`
  - 이 코드는 데이터베이스를 위험에 빠뜨릴 수 있습니다. 왜일까요?

## SQL 인젝션

- GUI의 'name' 텍스트 입력 상자에 사용자가 "Robert'; DROP TABLE students; --"를 입력했다고 가정해 보세요.
  - "SELECT dept_name FROM students WHERE name = '"+name+"';"
  - 결과 문장은 다음과 같이 됩니다:
  - "SELECT dept_name FROM students WHERE name = 'Robert'; DROP TABLE students; --';"
- **Prepared Statement**
  - 대신 사용자로부터 입력을 받을 때는 PreparedStatements를 사용하세요
  - PreparedStatement pStmt = conn.prepareStatement("Insert into instructor values(?,?,?)");
  - pStmt.setString(1, "88877");
  - pStmt.setString(2, "Perry");
  - pStmt.setString(3, "Finance");
  - pStmt.setInt(4, 125000);
  - pStmt.executeUpdate();
  - pStmt.setString(1, "88878");
  - pStmt.executeUpdate();
  - SELECT 쿼리의 경우 pStmt.executeQuery()를 사용하여 결과를 가져옵니다. 예: ResultSet rst = pStmt.executeQuery("...");
  - Prepared statement는 내부적으로 이스케이프된 따옴표를 사용합니다:
  - SELECT dept_name FROM students WHERE name = 'Robert'; DROP TABLE students; --'

## 메타데이터 기능

- **ResultSet 메타데이터**
  - 예: ResultSet rset을 얻기 위해 쿼리를 실행한 후:

```java
ResultSetMetaData rsmd = rset.getMetaData();
for (int i = 1; i <= rsmd.getColumnCount(); i++) {
    System.out.println(rsmd.getColumnName(i));
    System.out.println(rsmd.getColumnTypeName(i));
}
```

## 메타데이터 (계속)

- **DatabaseMetaData**
  - 데이터베이스에 대한 메타데이터를 가져오는 메서드 제공

```java
DatabaseMetaData dbmd = conn.getMetaData();
ResultSet rset = dbmd.getColumns(null, "univdb", "department", "%");
// 반환: 각 열에 대해 하나의 행;
// 행에는 COLUMN_NAME, TYPE_NAME 등 여러 속성이 있음
while (rset.next()) {
    System.out.println(rset.getString("COLUMN_NAME"));
    rset.getString("TYPE_NAME");
}
```

## Transaction Control in JDBC

- 기본적으로 각 SQL 문은 자동으로 commit되는 별도의 transaction으로 처리됨
  - 여러 개의 update가 있는 transaction에는 좋지 않은 방식
- Connection에서 자동 commit을 끌 수 있음
  - `conn.setAutoCommit(false);`
- 그러면 transaction을 명시적으로 commit하거나 rollback해야 함
  - `conn.commit();` 또는 `conn.rollback();`
- `conn.setAutoCommit(true)`는 자동 commit을 다시 켬

## Other JDBC Features

- Function과 procedure는 procedural PL로 구현 가능
  - 예: Oracle PL/SQL, MS TransactSQL
  - `CallableStatement cStmt1 = conn.prepareCall("(? = call_some_function(?))");`
  - `CallableStatement cStmt2 = conn.prepareCall("(call_some_procedure(?,?))");`
- Large object type 처리
  - `getBlob()`과 `getClob()`은 `getString()` 메서드와 유사하지만 Blob, Clob 타입 객체를 반환
  - `getBytes()`로 이 객체들에서 데이터를 가져옴
  - Java Blob이나 Clob 객체에 stream을 연결해 large object를 업데이트
    - `pstmt.setBlob(int parameterIndex, InputStream inputStream, long length)`

## SQLJ

- JDBC는 지나치게 동적이라 컴파일러가 에러를 잡을 수 없음
- SQLJ: Java에 embedded SQL

```java
#sql iterator deptInfoIter(String dept_name, int avgSal);
deptInfoIter iter = null;
#sql iter = { select dept_name, avg(salary)
              from instructor
              group by dept_name };
while (iter.next()) {
    String deptName = iter.dept_name();
    int avgSal = iter.avgSal();
    System.out.println(deptName + " " + avgSal);
}
iter.close();
```

## ODBC

- Open DataBase Connectivity(ODBC) 표준
- 다음을 위한 application program interface (API)
  - 데이터베이스와 connection 열기
  - query와 update 보내기
  - 결과 받기
- 원래 Basic과 C를 위해 정의되었고, 많은 언어로 버전 제공

## ODBC (Cont.)

- ODBC를 지원하는 각 DBMS는 client 프로그램과 link되어야 하는 "driver" 라이브러리 제공
- Client 프로그램이 ODBC API 호출을 하면, 라이브러리의 코드가 서버와 통신해 요청된 작업을 수행하고 결과를 가져옴
- ODBC 프로그램은 먼저 SQL environment를 할당한 다음 database connection handle을 할당
- `SQLConnect()`를 사용해 database connection을 열음
- `SQLConnect()`의 매개변수:
  - connection handle
  - 연결할 서버
  - user identifier
  - password

## ODBC Code

```c
int ODBCexample ()
{
    RETCODE error;
    HENV env;     /* environment */
    HDBC conn;    /* database connection */
    SQLAllocEnv(&env);
    SQLAllocConnect(env, &conn);
    SQLConnect(conn, "localhost", SQL_NTS, "bnam", SQL_NTS, "changethis", SQL_NTS);
    {
        // do actual work
        SQLDisconnect(conn);
        SQLFreeConnect(conn);
        SQLFreeEnv(env);
    }
}
```

## ODBC Code (Cont.)

- 프로그램은 `SQLExecDirect`를 사용해 SQL 명령을 DBMS로 보냄
- `SQLFetch()`를 사용해 결과 tuple을 가져옴
- `SQLBindCol()`은 query 결과의 attribute에 변수를 bind함
  - tuple이 fetch되면 attribute 값이 해당 C 변수에 저장됨
  - `SQLBindCol()`의 인자
    - ODBC stmt 변수, query 결과에서의 attribute 위치
    - SQL에서 C로의 type 변환
    - 변수의 주소
    - character array 같은 가변 길이 type의 경우:
      - 변수의 최대 길이
      - tuple이 fetch될 때 실제 길이를 저장할 위치
    - 참고: 길이 필드에 음수 값이 반환되면 null 값을 나타냄
- 좋은 프로그래밍은 모든 함수 호출 결과를 에러 체크해야 하지만, 간결성을 위해 대부분 생략함

## ODBC Code (Cont.)

- 프로그램의 주요 부분

```c
char deptname[80];
float salary;
int lenOut1, lenOut2;
HSTMT stmt;
char * sqlquery = "select dept_name, sum (salary) \
                   from instructor \
                   group by dept_name";
SQLAllocStmt(conn, &stmt);
ret = SQLExecDirect(stmt, sqlquery, SQL_NTS);
if (ret == SQL_SUCCESS) {
  SQLBindCol(stmt, 1, SQL_C_CHAR, deptname, 80, &lenOut1);
  SQLBindCol(stmt, 2, SQL_C_FLOAT, &salary, 0, &lenOut2);
  while (SQLFetch(stmt) == SQL_SUCCESS) {
    printf(" % s %g\n", deptname, salary);
  }
}
SQLFreeStmt(stmt, SQL_DROP);
```

## ODBC Prepared Statements

### Prepared Statement

- SQL statement가 준비됨: 데이터베이스에서 컴파일됨
- placeholder를 가질 수 있음: 예: `insert into account values(?,?,?)`
- placeholder에 실제 값을 넣어 반복 실행 가능

statement를 준비하려면:

```c
SQLPrepare(stmt, <SQL String>);
```

### 매개변수를 bind하려면

```c
SQLBindParameter(stmt, <parameter#>, type information and value omitted for simplicity..)
```

### statement를 실행하려면

```c
retcode = SQLExecute(stmt);
```

SQL injection 보안 위험을 피하려면 사용자 입력을 직접 사용해 SQL 문자열을 만들지 말고, prepared statement를 사용해 사용자 입력을 bind할 것

## Autocommit in ODBC

기본적으로 각 SQL 문은 자동으로 commit되는 별도의 transaction으로 처리됨

- Connection에서 자동 commit을 끌 수 있음
  - `SQLSetConnectOption(conn, SQL_AUTOCOMMIT, 0)`
- 그러면 transaction을 명시적으로 commit하거나 rollback해야 함
  - `SQLTransact(conn, SQL_COMMIT)` 또는
  - `SQLTransact(conn, SQL_ROLLBACK)`

## Procedural Extensions and Stored Procedures

- SQL은 declarative language
  - 각 query는 원하는 것을 선언하지만 로직은 알려주지 않음
  - 편리하지만 너무 제한적
  - 때로는 imperative 기능이 필요
    - if-then-else
    - for loop
    - while loop
    - 등
- Stored Procedure
  - 데이터베이스 내에서 procedure를 구현하고 저장 가능
  - call 문을 사용해 실행
  - DBMS 내에서 procedure 실행 (JDBC/ODBC와 달리)

## Function (PL/pgSQL)

```sql
CREATE [OR REPLACE] FUNCTION function_name (arguments)
RETURNS return_datatype AS $$
DECLARE
  declaration;
[...]
BEGIN
  < function_body >
  [...]
  RETURN { variable_name | value }
END;
$$
LANGUAGE plpgsql;
```

## Function (PL/pgSQL)

- **학생 수 총합을 반환하는 함수 정의하기**
  - 아래 코드는 STUDENT 테이블에서 count(*)를 사용해 총 학생 수를 계산하고 total 변수에 저장한 뒤 반환함
```sql
CREATE OR REPLACE FUNCTION total_students()
RETURNS integer AS $$
declare
  total integer;
BEGIN
  SELECT count(*) into total FROM STUDENT;
  RETURN total;
END;
$$ LANGUAGE pl/pgsql;
```
  - 사용 예시: 
```sql
SELECT dept_name, count(ID) 
FROM department NATURAL JOIN student
GROUP BY dept_name
HAVING count(ID) > total_students()/4;
```

## Table Function (PL/pgSQL)

- **함수가 결과로 relation을 반환할 수 있음**
- 예시: 특정 고객이 소유한 모든 계좌 반환하기
```sql
CREATE OR REPLACE FUNCTION instructors_of(dname char(20)) 
RETURNS TABLE (
  id varchar(5), ins_name varchar(20), 
  dept_name varchar(20), salary numeric(8,2)
) AS $$
BEGIN
  RETURN QUERY
  SELECT INS.ID, INS.name, INS.dept_name, INS.salary
  FROM instructor AS INS
  WHERE INS.dept_name = instructors_of.dname;
END;
$$ LANGUAGE pl/pgsql;
```
  - 사용법: 
```sql
select * from table (instructors_of('Finance'))
```

## If-Else Statement (PL/pgSQL)

- **Imperative conditional branch**
```
IF <condition> then
  <statements>
ELSIF <condition> then
  <statements>
ELSE
  <statements>
END IF
```
  - `<condition>`은 일반적인 Boolean 표현식임
  - END IF에는 공백이 포함되어 있지만 ELSIF에는 없음

- **학생 수 총합을 반환하는 함수 정의하기:**
```
DO $$
DECLARE std_age INT:= 20;
BEGIN
  IF std_age <= 18 THEN
    RAISE NOTICE 'student under 18';
  ELSE
    RAISE NOTICE 'student over 18';
  END IF;
END $$;
```

## Case Statement (PL/pgSQL)

- **Case 문법:**
```
CASE <expression>
WHEN <value> then
  <statements>
WHEN <value> then
  <statements>
...
ELSE
  <statements>
END CASE;
```
```
CASE
WHEN <condition> then
  <statements>
WHEN <condition> then
  <statements>
...
ELSE
  <statements>
END CASE;
```

- **Case 문 예시:**
```sql
DO $$
DECLARE
  letter VARCHAR(10);
  grade_value VARCHAR(10);
BEGIN
  FOR letter IN SELECT grade FROM takes
  LOOP
    grade_value := CASE letter
      WHEN 'A' THEN '4'
      WHEN 'B' THEN '3'
      WHEN 'C' THEN '2'
      ELSE 'other'
    END;
    RAISE NOTICE 'Grade: %, Value: %', letter, grade_value;
  END LOOP;
END $$;
```

## Simple Loop and While Loop (PL/pgSQL)

- **EXIT 또는 RETURN 문에 의해 종료될 때까지 반복**
```
LOOP
-- some computations
IF count > 0 THEN
EXIT; -- exit loop
END IF;
END LOOP;
```

- **boolean 표현식이 true로 평가되는 한 문장 시퀀스를 반복**
```
WHILE var1 > 0 AND var2 > 0 LOOP
-- some computations here
END LOOP;
```

## For Loop (PL/pgSQL)

- **정수 값 범위에 대해 반복하는 루프**
```
DO $$
DECLARE i INT;
BEGIN
FOR i IN 1..10 LOOP
RAISE NOTICE 'i = %', i;
END LOOP;
END $$;
```

- **쿼리 결과를 반복**
```
DO $$
DECLARE s RECORD;
BEGIN
FOR s IN 
SELECT id, name FROM student
LOOP
RAISE NOTICE 'id=%, name=%', s.id, s.name;
END LOOP;
END $$;
```

## Foreach Loop (PL/pgSQL)

- **FOREACH는 단일 요소가 아닌 배열의 slice를 반복함**
```
CREATE FUNCTION scan_rows(int[])
RETURNS void AS $$
DECLARE
  x int[];
BEGIN
  FOREACH x SLICE 1 IN ARRAY $1
  LOOP
    RAISE NOTICE 'row = %', x;
  END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## Triggers (PL/pgSQL)

- **트리거는 데이터베이스 수정의 부작용으로 시스템에 의해 자동으로 실행되는 문장임**
- 예시:
  - 계좌 잔액이 $500 미만으로 떨어지면 $10의 당좌 대월 수수료 부과
  - 직원의 급여 인상을 5% 이하로 제한
```
CREATE TRIGGER trigger-name
trigger-time trigger-event ON table-name
FOR EACH ROW
trigger-action;

trigger-time ∈ {BEFORE, AFTER}
trigger-event ∈ {INSERT, DELETE, UPDATE}
예) AFTER INSERT ON ...
BEFORE UPDATE ON
...
```

## Trigger Example (PL/pgSQL)

- **새로운 강사가 고용될 때 학과의 예산을 업데이트하는 트리거 생성:**
```
CREATE OR REPLACE FUNCTION update_budget()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.dept_name IS NOT NULL THEN
        UPDATE department
        SET budget = budget + NEW.salary
        WHERE dept_name = NEW.dept_name;
    END IF;
    RETURN NEW; -- new는 새로 삽입된 행을 참조
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_budget
AFTER INSERT ON instructor
FOR EACH ROW
EXECUTE PROCEDURE update_budget();
```

- **트리거 예시:**
```
bnam=> select * from department
where dept_name = 'Comp. Sci.';
 dept_name | building | budget 
----------+----------+--------
 Comp. Sci.| Taylor   | 100000.00
(1 row)

MariaDB> insert into instructor
values (88888, 'Nam', 'Comp. Sci.', 30000.00);
Query OK, 1 row affected (0.02 sec)

bnam=> select * from department
where dept_name = 'Comp. Sci.';
 dept_name | building | budget  
----------+----------+---------
 Comp. Sci.| Taylor   | 130000.00
(1 row)
```