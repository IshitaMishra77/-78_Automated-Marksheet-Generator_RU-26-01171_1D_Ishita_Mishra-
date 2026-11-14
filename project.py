import os 
import pandas as pd
def generate_marksheet(file_path,target_roll_no):
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}'was not found. ")
        return
    try:
        df=pd.read_csv(file_path,encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    df.columns = df.columns.str.strip()

    required_columns = ['RollNo', 'Name', 'Maths', 'Physics', 'Programming']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: CSV file is missing required columns: {', '.join(missing_columns)}")
        return

    valid_rows = []
    warnings = []
    target_found = False
    for index, row in df.iterrows():
        try:
            roll = int(row['RollNo'])
            if roll == target_roll_no:
                target_found = True
            name = str(row['Name']).strip()
            maths = float(row['Maths'])
            physics = float(row['Physics'])
            programming = float(row['Programming'])
        except (ValueError, TypeError, KeyError):
            warnings.append(
                f"(b) Warning: Row for roll {row.get('RollNo', 'Unknown')} "
                "skipped - non-numeric marks found"
            )
            continue

        if not (
            (0 <= maths <= 100) and
            (0 <= physics <= 100) and
            (0 <= programming <= 100)
        ):
            warnings.append(
                f"(b) Warning: Row for roll {roll} skipped - "
                "marks must be between 0 and 100."
            )
            continue

        valid_rows.append({
            'RollNo': roll,
            'Name': name,
            'Maths': maths,
            'Physics': physics,
            'Programming': programming,
        })
    valid_df = pd.DataFrame(valid_rows)
    match = valid_df[valid_df['RollNo'] == target_roll_no] if not valid_df.empty else valid_df
    if match.empty:
        if target_found:
            print(f'(a) Roll number {target_roll_no} was found, but its record has invalid data.')
        else:
            print(f'(a) Roll number {target_roll_no} not found.')
        for warning in warnings:
            print(warning)
        return
    student=match.iloc[0]
    m=student['Maths']
    p=student['Physics']
    pr=student['Programming']
    total=m+p+pr
    percentage=(total/300)*100
    if percentage>=90:
        grade="A+"
    elif percentage>=80:
        grade='A'
    elif percentage>=70:
        grade='B'
    elif percentage>=60:
        grade='C'
    elif percentage>=50:
        grade='D'
    elif percentage>=40:
        grade='E'
    else:
        grade="F"
    failed_subjects=[]
    if m<40:
        failed_subjects.append("Maths")
    if p<40:
        failed_subjects.append("Physics")
    if pr<40:
        failed_subjects.append("Programming")
    if failed_subjects:
        result=f'FAIL ({failed_subjects[0]} below 40)'
    else:
        result="PASS"
    print(f"Roll No: {int(student['RollNo'])} | Name: {student['Name']}")
    print(
        f"Maths: {int(m) if m.is_integer() else m} | "
        f"Physics: {int(p) if p.is_integer() else p} | "
        f"Programming: {int(pr) if pr.is_integer() else pr}"
    )
    print(
        f"Total: {int(total) if total.is_integer() else total}/300 | "
        f"Percentage: {percentage:.2f}%"
    )
    print(f"Grade: {grade} | Result: {result}")
if __name__=='__main__':
    file_name= r'C:\Users\hp\Documents\My Data Sources\marks.csv'
    try:
        user_input=input("Enter Roll no. to search: ")
        search_roll=int(user_input)
        print('-'*40)
        generate_marksheet(file_name, search_roll)
        print('-'*40)
    except ValueError:
        print('Please enter a valid numeric roll no. ')

