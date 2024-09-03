class TextFilter:
    @staticmethod
    def remove_noise(
        text: str,
        min_line_len: int = 3,
        nchar_real_line: int = 36,
        max_line_count: int = 300
    ) -> str:
        """Remove contextual noise from the text.

        Parameters
        ----------
        text : str
            Normally the `text extracted from a webpage`. It can thus contain
            - text from navigation bars
            - text from footers
            - strange links
            - etc.
        max_char_len : int, optional
            _description_, by default 2000
        min_paragraph_len : int, optional
            _description_, by default 3
        """
        lines = text.split("\n")

        # Drop obvious bad lines
        lines = [
            line for line in lines if (
                len(line) >= min_line_len
            )
        ]

        # Identify the start of real content
        # TODO: use nchar of all lines + moving average of x-lines
        start_idx = 0
        for idx, line in enumerate(lines):
            start_idx = idx
            if len(line) >= nchar_real_line:
                break
        start_idx = max(0, start_idx-1)
        lines = lines[start_idx:start_idx+max_line_count]

        return "\n".join(lines)
