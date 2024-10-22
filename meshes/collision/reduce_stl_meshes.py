import os
import pymeshlab

def reduce_mesh(input_file, output_file, target_reduction):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_file)

    # 현재 면 수 계산
    current_faces = ms.current_mesh().face_number()

    # 목표 면 수 계산
    target_faces = int(current_faces * (1 - target_reduction))

    # 메시 간소화
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=target_faces)

    # 결과 저장
    ms.save_current_mesh(output_file)

def process_directory(directory, target_reduction=0.5):
    # 'reduced' 폴더 생성
    reduced_dir = os.path.join(directory, "reduced")
    if not os.path.exists(reduced_dir):
        os.makedirs(reduced_dir)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.stl'):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(reduced_dir, filename)

            print(f"Processing {filename}...")
            try:
                reduce_mesh(input_path, output_path, target_reduction)
                print(f"Reduced mesh saved as {output_path}")
            except pymeshlab.pmeshlab.PyMeshLabException as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    directory = "."  # 현재 디렉토리
    target_reduction = 0.5  # 50% 감소

    process_directory(directory, target_reduction)
    print("All STL files have been processed.")

# 사용 가능한 필터 목록 출력
print("\nAvailable filters:")
for filter_name in dir(pymeshlab.MeshSet):
    if not filter_name.startswith('__') and callable(getattr(pymeshlab.MeshSet, filter_name)):
        print(filter_name)
