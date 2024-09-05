# Copyright 2024  darryl mcculley

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

try:
    from IPython.core.magic import Magics, magics_class, cell_magic
    from IPython.display import Markdown, display
    from IPython import get_ipython
    from openai import OpenAI
except ImportError:
    raise ImportError("`ipython` and `openai` required for magic.")

from . import delta

from json import dumps

@magics_class
class magic (Magics):
    def __init__(self, shell, delta:delta):
        super(magic, self).__init__(shell)
        self.delta = delta
        self.__openai_chat_history = []
        self.client = OpenAI()

    @cell_magic
    def sql(self, line, cell):
        return self.delta.sql(query=cell, dtype="polars")
    
    @cell_magic
    def ai(self, line, cell):
        context = ""
        for table in self.delta.tables:
            schema = self.delta.schema(table=table)
            if schema: context += f"- {table}: {schema}\n"

        messages = [
            {"role": "system", "content": (
                "answer the user's question. "
                "below is the data they have access to. "
                "data can be accessed via sql."
            )},
            {"role": "user", "content": f"[question]\n{cell}\n[available data]" + context}
        ]
        for question, answer in self.__openai_chat_history:
            messages.append({"role": "user", "content":question})
            messages.append({"role": "assistant", "content":answer})

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        response = completion.choices[0].message.content
        self.__openai_chat_history.append((cell, response))
        return display(Markdown(response))

def enable(delta:delta):
    ipython = get_ipython()
    if ipython: ipython.register_magics(magic(ipython, delta))