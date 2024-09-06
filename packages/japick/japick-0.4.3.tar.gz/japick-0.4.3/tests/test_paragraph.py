from japick.lines import Line
from japick.paragraph import Paragraph, Pos, parse_paragraph
from japick.syntax import NULL_SYMBOL


class TestParagraph:
    def test_body(self):
        target = Paragraph(
            0,
            0,
            [
                "  これはテスト。",
                f"  次の {NULL_SYMBOL * 2}テスト{NULL_SYMBOL * 2}。",
            ],
        )
        assert (
            target.body
            == """これはテスト。
次の テスト。"""
        )

    def test_body_memoize(self):
        target = Paragraph(0, 0, [], _body="Memoized")
        assert target.body == "Memoized"

    def test_as_original_pos(self):
        target = Paragraph(
            0,
            0,
            [
                "  これはテスト。",
                f"  次の {NULL_SYMBOL * 2}テスト{NULL_SYMBOL * 2}。",
            ],
        )
        # これはテスト。
        # 次の テ[HERE]スト。
        actual = target.as_original_pos(12)
        assert actual == Pos(1, 8)

    def test_as_original_pos_greedy_lazy(self):
        target = Paragraph(
            0,
            0,
            [f"次の {NULL_SYMBOL * 2}テスト{NULL_SYMBOL * 2}。"],
        )
        # 次の テスト[HERE]。
        actual = target.as_original_pos(3, lazy=False)
        assert actual == Pos(0, 5)
        actual = target.as_original_pos(6, lazy=False)
        assert actual == Pos(0, 10)
        actual = target.as_original_pos(3, lazy=True)
        assert actual == Pos(0, 3)
        actual = target.as_original_pos(6, lazy=True)
        assert actual == Pos(0, 8)

    def test_as_original_index(self):
        target = Paragraph(
            5,
            200,
            [
                "    これはテスト。",
                "      これは2行目",
            ],
        )
        actual = target.as_original_index(11)
        assert actual == 221

    def test_as_original_index_lazy(self):
        target = Paragraph(0, 0, [f"これは{NULL_SYMBOL}テスト。"])
        assert target.as_original_index(3, lazy=False) == 4
        assert target.as_original_index(3, lazy=True) == 3


def test_parse_paragraph_list():
    actual = parse_paragraph(
        [
            Line("文"),
            Line("リスト", is_list=True),
            Line("リスト2", is_list=True),
        ]
    )
    assert list(actual) == [
        Paragraph(0, 0, ["文"]),
        Paragraph(1, 2, ["リスト"], is_list=True),
        Paragraph(2, 6, ["リスト2"], is_list=True),
    ]


def test_parse_paragraph_heading():
    actual = list(
        parse_paragraph(
            [
                Line("見出し", is_head=True),
                Line("文"),
                Line("文2"),
            ]
        )
    )
    assert actual == [
        Paragraph(0, 0, ["見出し"], is_head=True),
        Paragraph(1, 4, ["文", "文2"]),
    ]


def test_parse_paragraph_multiple():
    actual = parse_paragraph(
        [
            Line("Test", is_ignore=True),
            Line("文1"),
            Line("文2"),
            Line("", is_ignore=True),
            Line("文3"),
            Line("文4"),
        ]
    )
    assert list(actual) == [
        Paragraph(1, 5, ["文1", "文2"]),
        Paragraph(4, 12, ["文3", "文4"]),
    ]
