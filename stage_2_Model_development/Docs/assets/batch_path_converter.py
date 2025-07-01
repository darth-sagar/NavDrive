import csv
from pathlib import Path

# Configuration
INPUT_ROOT = Path(r"C:\Users\USER\OneDrive\Desktop\Model\data_runs")
OUTPUT_ROOT = Path(r"C:\Users\USER\OneDrive\Desktop\Model\converted_data_run")
CSV_COLUMN_NAME = "image_path"

def process_directory():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    
    for run_dir in sorted(INPUT_ROOT.glob("run_*")):
        if not run_dir.is_dir():
            continue

        csv_file = run_dir / f"{run_dir.name}.csv"
        if not csv_file.exists():
            print(f"⚠️ Skipping {run_dir.name} - CSV file not found")
            continue

        output_dir = OUTPUT_ROOT / run_dir.relative_to(INPUT_ROOT)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_csv = output_dir / csv_file.name

        print(f"\n🔍 Processing {run_dir.name}...")
        error_count = 0

        with open(csv_file, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            
            if CSV_COLUMN_NAME not in reader.fieldnames:
                print(f"❌ Critical error: Missing '{CSV_COLUMN_NAME}' column")
                continue
                
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()

            for row_num, row in enumerate(reader, 1):
                try:
                    # Safely get and verify the image path
                    file_path = row.get(CSV_COLUMN_NAME, '')
                    
                    # Handle missing/empty paths
                    if not isinstance(file_path, str) or not file_path.strip():
                        error_count += 1
                        print(f"⚠️ Row {row_num}: Invalid path '{file_path}' - keeping original")
                        file_path = file_path or ''  # Ensure string type
                    
                    # Construct new path
                    new_path = OUTPUT_ROOT / run_dir.name / file_path.replace('/', '\\')
                    row[CSV_COLUMN_NAME] = str(new_path)
                    writer.writerow(row)

                except Exception as e:
                    error_count += 1
                    print(f"❌ Error at row {row_num}: {str(e)}")
                    print(f"    Raw row data: {row}")
                    
                    # Write original row to preserve data
                    writer.writerow(row)

        print(f"✅ Finished {run_dir.name} with {error_count} errors")

if __name__ == "__main__":
    print("🚀 Starting CSV conversion...")
    process_directory()
    print("\n🎉 Conversion completed. Check output files for integrity.")