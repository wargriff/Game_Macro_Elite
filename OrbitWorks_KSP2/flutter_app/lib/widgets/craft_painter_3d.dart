import 'dart:math' as math;
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

import '../models/craft.dart';

/// Procedural KSP2-like craft preview (not proprietary game meshes).
class CraftPreview3D extends StatefulWidget {
  final Craft craft;
  final bool autoRotate;

  const CraftPreview3D({
    super.key,
    required this.craft,
    this.autoRotate = true,
  });

  @override
  State<CraftPreview3D> createState() => _CraftPreview3DState();
}

class _CraftPreview3DState extends State<CraftPreview3D>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  double _yaw = 0.55;
  double _pitch = -0.25;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 12))
      ..addListener(() {
        if (widget.autoRotate) {
          setState(() => _yaw = _ctrl.value * math.pi * 2);
        }
      });
    if (widget.autoRotate) _ctrl.repeat();
  }

  @override
  void didUpdateWidget(covariant CraftPreview3D oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.autoRotate && !_ctrl.isAnimating) {
      _ctrl.repeat();
    } else if (!widget.autoRotate && _ctrl.isAnimating) {
      _ctrl.stop();
    }
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanUpdate: (d) {
        setState(() {
          _yaw += d.delta.dx * 0.01;
          _pitch = (_pitch + d.delta.dy * 0.008).clamp(-1.0, 0.6);
        });
      },
      child: CustomPaint(
        painter: _CraftPainter(
          craft: widget.craft,
          yaw: _yaw,
          pitch: _pitch,
        ),
        child: const SizedBox.expand(),
      ),
    );
  }
}

class _Vec3 {
  final double x, y, z;
  const _Vec3(this.x, this.y, this.z);
  _Vec3 operator +(_Vec3 o) => _Vec3(x + o.x, y + o.y, z + o.z);
  _Vec3 operator -(_Vec3 o) => _Vec3(x - o.x, y - o.y, z - o.z);
  _Vec3 operator *(double s) => _Vec3(x * s, y * s, z * s);
}

class _Face {
  final List<_Vec3> pts;
  final Color color;
  const _Face(this.pts, this.color);
}

class _CraftPainter extends CustomPainter {
  final Craft craft;
  final double yaw;
  final double pitch;

  _CraftPainter({required this.craft, required this.yaw, required this.pitch});

  @override
  void paint(Canvas canvas, Size size) {
    final bg = Paint()
      ..shader = ui.Gradient.radial(
        Offset(size.width * 0.55, size.height * 0.35),
        size.shortestSide * 0.8,
        const [Color(0xFF15263A), Color(0xFF060A12)],
      );
    canvas.drawRect(Offset.zero & size, bg);

    // stars
    final star = Paint()..color = const Color(0x88B8D4FF);
    final rnd = math.Random(42);
    for (var i = 0; i < 80; i++) {
      canvas.drawCircle(
        Offset(rnd.nextDouble() * size.width, rnd.nextDouble() * size.height * 0.7),
        rnd.nextDouble() * 1.4 + 0.4,
        star,
      );
    }

    // ground grid
    final grid = Paint()
      ..color = const Color(0x331E3A4A)
      ..strokeWidth = 1;
    for (var i = -8; i <= 8; i++) {
      final a = _project(_Vec3(i.toDouble(), 0, -8), size, yaw, pitch);
      final b = _project(_Vec3(i.toDouble(), 0, 8), size, yaw, pitch);
      final c = _project(_Vec3(-8, 0, i.toDouble()), size, yaw, pitch);
      final d = _project(_Vec3(8, 0, i.toDouble()), size, yaw, pitch);
      canvas.drawLine(a, b, grid);
      canvas.drawLine(c, d, grid);
    }

    final faces = _buildFaces(craft);
    faces.sort((a, b) {
      final za = a.pts.map((p) => _rot(p, yaw, pitch).z).reduce((x, y) => x + y) / a.pts.length;
      final zb = b.pts.map((p) => _rot(p, yaw, pitch).z).reduce((x, y) => x + y) / b.pts.length;
      return za.compareTo(zb);
    });

    for (final f in faces) {
      final path = Path();
      for (var i = 0; i < f.pts.length; i++) {
        final o = _project(f.pts[i], size, yaw, pitch);
        if (i == 0) {
          path.moveTo(o.dx, o.dy);
        } else {
          path.lineTo(o.dx, o.dy);
        }
      }
      path.close();
      final depth = _rot(f.pts.first, yaw, pitch).z;
      final shade = (0.55 + depth * 0.08).clamp(0.35, 0.95);
      final fill = Color.fromRGBO(
        (f.color.r * 255.0 * shade).round().clamp(0, 255),
        (f.color.g * 255.0 * shade).round().clamp(0, 255),
        (f.color.b * 255.0 * shade).round().clamp(0, 255),
        1,
      );
      canvas.drawPath(path, Paint()..color = fill);
      canvas.drawPath(
        path,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1
          ..color = Colors.white.withValues(alpha: 0.12),
      );
    }
  }

  List<_Face> _buildFaces(Craft craft) {
    final cat = craft.category;
    final preview = craft.preview;
    if (cat == 'starship' || preview == 'starship') return _starship();
    if (cat == 'starlink' || cat == 'comms' || cat == 'data' || preview == 'starlink') {
      return cat == 'starlink' || preview == 'starlink' ? _starlink() : _sat();
    }
    if (cat == 'rovers') return _rover();
    return _rocket();
  }

  List<_Face> _box(double cx, double cy, double cz, double w, double h, double d, Color c) {
    final x0 = cx - w / 2, x1 = cx + w / 2;
    final y0 = cy, y1 = cy + h;
    final z0 = cz - d / 2, z1 = cz + d / 2;
    final p = [
      _Vec3(x0, y0, z0),
      _Vec3(x1, y0, z0),
      _Vec3(x1, y1, z0),
      _Vec3(x0, y1, z0),
      _Vec3(x0, y0, z1),
      _Vec3(x1, y0, z1),
      _Vec3(x1, y1, z1),
      _Vec3(x0, y1, z1),
    ];
    return [
      _Face([p[0], p[1], p[2], p[3]], c),
      _Face([p[5], p[4], p[7], p[6]], c),
      _Face([p[4], p[0], p[3], p[7]], Color.lerp(c, Colors.black, 0.15)!),
      _Face([p[1], p[5], p[6], p[2]], Color.lerp(c, Colors.white, 0.08)!),
      _Face([p[3], p[2], p[6], p[7]], Color.lerp(c, Colors.white, 0.12)!),
      _Face([p[4], p[5], p[1], p[0]], Color.lerp(c, Colors.black, 0.25)!),
    ];
  }

  List<_Face> _cyl(double cx, double cy, double cz, double r, double h, Color c, {int seg = 10}) {
    final faces = <_Face>[];
    for (var i = 0; i < seg; i++) {
      final a0 = i / seg * math.pi * 2;
      final a1 = (i + 1) / seg * math.pi * 2;
      final p0 = _Vec3(cx + math.cos(a0) * r, cy, cz + math.sin(a0) * r);
      final p1 = _Vec3(cx + math.cos(a1) * r, cy, cz + math.sin(a1) * r);
      final p2 = _Vec3(cx + math.cos(a1) * r, cy + h, cz + math.sin(a1) * r);
      final p3 = _Vec3(cx + math.cos(a0) * r, cy + h, cz + math.sin(a0) * r);
      faces.add(_Face([p0, p1, p2, p3], i.isEven ? c : Color.lerp(c, Colors.black, 0.08)!));
    }
    return faces;
  }

  List<_Face> _starship() {
    const steel = Color(0xFFC9CED6);
    const tile = Color(0xFF3A342E);
    const dark = Color(0xFF2A2E36);
    return [
      ..._cyl(0, 0, 0, 1.15, 4.4, steel),
      ..._cyl(0, 3.6, 0, 1.16, 0.35, tile),
      ..._cyl(0, 4.5, 0, 1.05, 3.6, steel),
      ..._cyl(0, 5.0, 0, 1.06, 0.25, tile),
      ..._box(1.15, 6.8, 0, 0.12, 1.4, 1.5, const Color(0xFFA8AEB8)),
      ..._box(-1.15, 6.8, 0, 0.12, 1.4, 1.5, const Color(0xFFA8AEB8)),
      // nose approx
      ..._cyl(0, 8.1, 0, 0.75, 1.2, const Color(0xFFD7DDE6), seg: 8),
      ..._cyl(0, 9.1, 0, 0.35, 0.7, const Color(0xFFD7DDE6), seg: 8),
      // engines
      for (var i = 0; i < 9; i++)
        ..._cyl(
          math.cos(i / 9 * math.pi * 2) * 0.7,
          -0.35,
          math.sin(i / 9 * math.pi * 2) * 0.7,
          0.12,
          0.35,
          dark,
          seg: 6,
        ),
    ];
  }

  List<_Face> _starlink() {
    const bus = Color(0xFF9AA3B0);
    const panel = Color(0xFF1A4A9A);
    return [
      ..._box(0, 0.2, 0, 1.5, 0.12, 0.55, bus),
      ..._box(0, 0.22, 0, 2.4, 0.04, 0.7, panel),
      ..._box(0.4, 0.35, 0, 0.35, 0.2, 0.25, const Color(0xFFC8CCD4)),
      ..._cyl(-0.45, 0.35, 0, 0.03, 0.55, const Color(0xFFDDDDDD), seg: 6),
    ];
  }

  List<_Face> _sat() {
    return [
      ..._box(0, 0.2, 0, 0.95, 0.4, 0.75, const Color(0xFFC4C8D0)),
      ..._box(-1.4, 0.35, 0, 1.6, 0.05, 0.55, const Color(0xFF1A4080)),
      ..._box(1.4, 0.35, 0, 1.6, 0.05, 0.55, const Color(0xFF1A4080)),
      ..._cyl(0, 0.7, 0, 0.35, 0.08, Colors.white, seg: 12),
    ];
  }

  List<_Face> _rocket() {
    const body = Color(0xFFE8E2D6);
    const stripe = Color(0xFFD4A574);
    return [
      ..._cyl(0, 0, 0, 0.7, 1.6, body),
      ..._cyl(0, 1.6, 0, 0.62, 1.4, stripe),
      ..._cyl(0, 3.0, 0, 0.55, 1.2, body),
      ..._cyl(0, 4.2, 0, 0.35, 0.9, const Color(0xFFF2EEE6), seg: 8),
      ..._cyl(0, 4.9, 0, 0.12, 0.5, const Color(0xFFF2EEE6), seg: 6),
      ..._box(0.75, 0.1, 0, 0.08, 0.8, 0.45, const Color(0xFFB0A090)),
      ..._box(-0.75, 0.1, 0, 0.08, 0.8, 0.45, const Color(0xFFB0A090)),
      ..._cyl(0, -0.4, 0, 0.28, 0.4, const Color(0xFF333840), seg: 8),
    ];
  }

  List<_Face> _rover() {
    return [
      ..._box(0, 0.3, 0, 1.5, 0.35, 1.0, const Color(0xFFC4A574)),
      ..._box(0, 0.65, 0, 0.55, 0.4, 0.55, const Color(0xFF8890A0)),
      ..._cyl(0, 1.05, 0, 0.05, 0.7, const Color(0xFFB0B4BC), seg: 6),
      ..._box(0, 1.7, 0, 0.28, 0.14, 0.14, const Color(0xFF333840)),
      for (final o in const [(-0.55, -0.45), (-0.55, 0.45), (0.55, -0.45), (0.55, 0.45)])
        ..._cyl(o.$1, 0.0, o.$2, 0.22, 0.2, const Color(0xFF222428), seg: 8),
    ];
  }

  _Vec3 _rot(_Vec3 v, double yaw, double pitch) {
    final cy = math.cos(yaw), sy = math.sin(yaw);
    final cp = math.cos(pitch), sp = math.sin(pitch);
    var x = v.x * cy - v.z * sy;
    var z = v.x * sy + v.z * cy;
    final y = v.y * cp - z * sp;
    z = v.y * sp + z * cp;
    return _Vec3(x, y, z);
  }

  Offset _project(_Vec3 v, Size size, double yaw, double pitch) {
    final r = _rot(v, yaw, pitch);
    final scale = size.shortestSide * 0.085;
    final cx = size.width * 0.55;
    final cy = size.height * 0.72;
    return Offset(cx + r.x * scale, cy - r.y * scale);
  }

  @override
  bool shouldRepaint(covariant _CraftPainter oldDelegate) =>
      oldDelegate.yaw != yaw || oldDelegate.pitch != pitch || oldDelegate.craft.id != craft.id;
}
