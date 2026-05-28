-- Cartographer 2D SLAM 配置文件
include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",            -- 全局地图坐标系
  tracking_frame = "base_link", -- 机器人本体坐标系
  published_frame = "odom",     -- 发布位姿相对的坐标系
  odom_frame = "odom",
  provide_odom_frame = false,   -- 由 Gazebo 差速插件提供 odom→base_link TF
  publish_frame_projected_to_2d = true, -- 2D建图，投影到平面
  use_odometry = true,          -- 使用里程计数据辅助建图
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,          -- 接收1路激光扫描数据
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- 启用2D建图器
MAP_BUILDER.use_trajectory_builder_2d = true

-- 子图参数：每35帧激光数据构建一个子图
TRAJECTORY_BUILDER_2D.submaps.num_range_data = 35
TRAJECTORY_BUILDER_2D.min_range = 0.1   -- 最小测距范围
TRAJECTORY_BUILDER_2D.max_range = 5.0   -- 最大测距范围（与激光雷达一致）
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 5.0

-- Ceres 扫描匹配器权重：影响建图精度
TRAJECTORY_BUILDER_2D.use_imu_data = false -- 无IMU，仅用里程计+激光
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.occupied_space_weight = 10.
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight = 5.
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.rotation_weight = 5.

-- 闭环检测：每90个节点优化一次，min_score 控制闭环匹配阈值
POSE_GRAPH.optimization_problem.huber_scale = 1e1
POSE_GRAPH.optimize_every_n_nodes = 90
POSE_GRAPH.constraint_builder.min_score = 0.55

return options
