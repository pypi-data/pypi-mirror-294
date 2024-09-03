import functools
import sys
import re
from pathlib import Path
import itertools
from abc import ABC, abstractmethod
from rebrick.Core import RefactorReplaceOp, RefactorToolkit

def migration(from_version: str, to_version: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result
        wrapper._from_version = from_version
        wrapper._to_version = to_version
        return wrapper
    return decorator

@migration("0.9.2", "0.9.3")
def snakecaseify_methods(documents):
    ops = []
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Vec3.fromXYZ", "from_xyz"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Vec3.angleBetweenVectors", "angle_between_vectors"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Vec3.getOrthogonalUnitVector", "get_orthogonal_unit_vector"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Quat.angleAxis", "angle_axis"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Quat.fromTo", "from_to"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Quat.fromXYZW", "from_xyzw"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.AffineTransform.fromAxes", "from_axes"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.AffineTransform.inverseOf", "inverse_of"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.AffineTransform.transformVec3Point", "transform_vec3_point"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.AffineTransform.transformVec3Vector", "transform_vec3_vector"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix3x3.fromRowMajor", "from_row_major"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix3x3.fromRows", "from_rows"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix3x3.fromColumns", "from_columns"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.fromRowMajor", "from_row_major"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.fromRows", "from_rows"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.fromColumns", "from_columns"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.fromVec3Quat", "from_vec3_quat"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.getAffineTranslation", "get_affine_translation"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Matrix4x4.getAffineRotation", "get_affine_rotation"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Functions.harmonicMean", "harmonic_mean"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Math.Line.fromPoints", "from_points"))

    return list(map(lambda op: ReplaceOp(op), ops))

@migration("0.9.3", "0.10.0")
def snakecaseify_methods_093(documents):
    ops = []
    # ValueOutputSignal
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromAngle", "from_angle"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromAngularVelocity1D", "from_angular_velocity_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromDistance", "from_distance"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromForce1D", "from_force_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromVelocity1D", "from_velocity_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromTorque1D", "from_torque_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromAcceleration3D", "from_acceleration_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromAngularAcceleration3D", "from_angular_acceleration_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromAngularVelocity3D", "from_angular_velocity_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromForce3D", "from_force_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromTorque3D", "from_torque_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromVelocity3D", "from_velocity_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromPosition3D", "from_position_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.fromRPY", "from_rpy"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.isReal", "is_real"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asReal", "as_real"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asVec3", "as_vec3"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asAngle", "as_angle"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asAngularVelocity1D", "as_angular_velocity_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asDistance", "as_distance"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asForce1D", "as_force_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asVelocity1D", "as_velocity_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asTorque1D", "as_torque_1d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asAcceleration3D", "as_acceleration_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asAngularAcceleration3D", "as_angular_acceleration_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asAngularVelocity3D", "as_angular_velocity_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asForce3D", "as_force_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asTorque3D", "as_torque_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asVelocity3D", "as_velocity_3d"))
    ops.extend(RefactorToolkit.renameMethod(documents, "Physics.Signals.ValueOutputSignal.asPosition3D", "as_position_3d"))

    return list(map(lambda op: ReplaceOp(op), ops))

@migration("0.9.3", "0.10.0")
def snakecaseify_methods_093(documents):
    ops = []
    ops.extend(RefactorToolkit.renameMethod(documents, "Robotics.Signals.RobotInputSignal.fromValues", "from_values"))
    return list(map(lambda op: ReplaceOp(op), ops))

def split_version(v):
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', v)

    if not match:
        raise ValueError("Invalid version format")

    return tuple(int(part) for part in match.groups())

def collect_migrations(from_version, to_version):
    migrations = filter(lambda obj: (
        callable(obj)
        and hasattr(obj, '_from_version')
        and hasattr(obj, '_to_version')
        and split_version(from_version) <= split_version(obj._from_version)
        and split_version(obj._from_version) < split_version(to_version)
    ), [obj for _, obj in globals().items()])

    return sorted(list(migrations), key=lambda m: split_version(m._from_version))

class MigrateOp(ABC):
    @abstractmethod
    def apply_to(self):
        pass

class ReplaceOp(MigrateOp):
    def __init__(self, op: RefactorReplaceOp):
        self.path = Path(op.source_id)
        self.from_line = op.from_line
        self.from_column = op.from_column
        self.end_line = op.end_line
        self.end_column = op.end_column
        self.new_content = op.new_content

    def __str__(self):
        return f"{{{self.path}, {self.from_line}, {self.from_column}, {self.end_line}, {self.end_column}, {self.new_content} }}"

    @staticmethod
    def apply_many(ops, lines):
        # There can be multiple ops per line, we need to run them in order sorted by column
        for _, line_group in itertools.groupby(ops, lambda op: op.from_line):
            offset = 0
            for op in sorted(line_group, key = lambda op: op.from_column):
                lines = op.apply_to(lines, offset)
                offset += len(op.new_content) - op.end_column + op.from_column
        return lines

    def apply_to(self, lines, offset):

        if self.end_line != self.from_line:
            print("Multiple line replace ops are not supported", file=sys.stderr)
            return

        target_line = lines[self.from_line - 1]

        lines[self.from_line - 1] = target_line[:(self.from_column + offset - 1)] + self.new_content + target_line[(self.end_column + offset - 1):]

        return lines
