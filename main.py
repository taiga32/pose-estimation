import cv2
import mediapipe as mp
import numpy as np
import rerun as rr
import os
import glob

# data/original配下のMP4ファイルを検索
video_dir = "data/original"
video_files = glob.glob(os.path.join(video_dir, "*.mp4"))

if not video_files:
    print(f"エラー: {video_dir}にMP4ファイルが見つかりません")
    exit(1)

# 最初のMP4ファイルを使用（複数ある場合）
video_path = video_files[0]
print(f"読み込むビデオファイル: {video_path}")

# rerunの初期化
rr.init("pose_estimation_demo", spawn=True)

# 最新バージョンのrerunならVideoFileを使用
try:
    # 動画ファイルをRerunに直接送信
    rr.log("video_file", rr.VideoFile(video_path))
    print("VideoFileとして送信しました")
except AttributeError:
    print("古いRerunバージョンのため、フレームごとに送信します")

# MediaPipe Poseの初期化
mp_pose = mp.solutions.pose

# ビデオキャプチャを開く
cap = cv2.VideoCapture(video_path)

with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    if not cap.isOpened():
        print(f"Error: ビデオファイル {video_path} を開けませんでした")
    else:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)
            image.flags.writeable = True

            # 時間シーケンスを設定（フレームごとに）
            # rr.set_time_sequence("frame", frame_idx)
            rr.set_time("time", timestamp=frame_idx)  # Seconds since unix epoch
            # timestamp = rr.TimePoint(frame_idx)
            
            # rerunで画像を送信（VideoFileがない場合や補助的な表示用）
            rr.log(f"frame", rr.Image(image))

            # # rerunでランドマークを可視化
            # if results.pose_landmarks:
            #     landmarks = results.pose_landmarks.landmark
            #     points = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])
            #     rr.log(f"frame/{frame_idx}/pose", rr.Points3D(points))

            frame_idx += 1
            
            # 進捗表示（20フレームごと）
            if frame_idx % 20 == 0:
                print(f"処理中: フレーム {frame_idx}")

            # 'q'キーで終了（OpenCVウィンドウがある場合）
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()

print(f"処理完了: 合計 {frame_idx} フレーム")