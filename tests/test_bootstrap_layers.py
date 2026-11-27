import os

from utils.bootstrap_layers import SamTemplate


def test_bootstrap_layers_preserves_newer_function_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    template = tmp_path / "template.yaml"
    template.write_text(
        """\
Resources:
  Layer:
    Type: AWS::Serverless::LayerVersion
  Function:
    Type: AWS::Serverless::Function
    Properties:
      Layers: !If [IsNotLocal, [!Ref Layer], !Ref 'AWS::NoValue']
"""
    )
    layer = tmp_path / ".aws-sam/build/Layer/python"
    function = tmp_path / ".aws-sam/build/Function"
    layer.mkdir(parents=True)
    function.mkdir(parents=True)
    (layer / "older.py").write_text("layer")
    (function / "older.py").write_text("function")
    os.utime(layer / "older.py", (100, 100))
    os.utime(function / "older.py", (200, 200))
    (layer / "newer.py").write_text("layer")
    (function / "newer.py").write_text("function")
    os.utime(function / "newer.py", (100, 100))
    os.utime(layer / "newer.py", (200, 200))
    (layer / "new.py").write_text("new")

    SamTemplate(template)

    assert (function / "older.py").read_text() == "function"
    assert (function / "newer.py").read_text() == "layer"
    assert (function / "new.py").read_text() == "new"
