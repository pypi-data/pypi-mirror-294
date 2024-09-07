import argparse, json, termcolor, time
import asyncio
from datetime import datetime
from refact import chat_client


DUMP_PREFIX = datetime.now().strftime("%Y%m%d-%H%M%S")

# MODEL = "gpt-4-turbo"
# MODEL = "gpt-4o"
# MODEL = "gpt-3.5-turbo-1106"  # $1, multi call works
# MODEL = "gpt-3.5-turbo-0125"    # $0.50
MODEL = "gpt-3.5-turbo"    # $0.50


SYSTEM_PROMPT = '''
You are Refact Chat, a coding assistant.

Follow these steps to answer the user queries.

Step 1 - Start with triple quotes ("""). Decide if it's a question related to the current project, write you reasoning inside the triple quotes.

Step 2 - If it's about the current project, decide whether you have enough information already present in the context. If not, write which
calls will be most useful to collect the necessary context, list up to 5 calls. `definition` and `references` are most useful when you have
specific function/class name, and `search_workspace` when you need to find a similar code or text or topic in the project.

Step 3 - Close the triple quotes (""").

Step 4 - Answer the question normally, or call tools in parallel following your plan.

IF YOU PLANNED SEVERAL CALLS, CALL MULTIPLE TOOLS IN PARALLEL.
'''


# Example 1

# Question
# explain code
# ```
# def f(x: MyClass1, y: MyClass2):
#     return x + y
# ```

# Answer
# definition(symbol="MyClass1") definition(symbol="MyClass2") search_workspace(query="def f(x: MyClass1, y: MyClass2)")

# Example 2

# Question
# Why is this outdated in fastapi?
# ```
# @validator('input')
# ```

# Answer
# `@validator('input')` was used in older versions of FastAPI to define a validation function for a request body field. However, in newer versions of FastAPI, the `@validator` decorator has been replaced with the `Field` class from the `pydantic` library.


LOCATION = """
Current dir: code_horrible/hibernate-orm/
Current dir summary:
Hibernate ORM is a powerful object/relational mapping solution for Java, and makes it easy to develop persistence logic for applications, libraries, and frameworks.
Hibernate implements JPA, the standard API for object/relational persistence in Java, but also offers an extensive set of features and APIs which go beyond the specification.
Listing folder code_horrible/hibernate-orm/
       192     dir checkerstubs/
        60    file ls.vecdb
       448     dir design/
       128     dir hibernate-micrometer/
       128     dir documentation/
       192     dir tooling/
       416     dir databases/
       256     dir local-build-plugins/
       128     dir drivers/
      7530    file release-announcement.adoc
       128     dir hibernate-vector/
       128     dir hibernate-community-dialects/
       320     dir hibernate-spatial/
       128     dir hibernate-proxool/
       128     dir hibernate-ucp/
       320     dir ci/
       128     dir hibernate-core/
      6037    file MAINTAINERS.md
       128     dir hibernate-jfr/
       128     dir hibernate-vibur/
      1456    file hibernate_logo.gif
       256     dir etc/
      1802    file branching.adoc
       128     dir hibernate-jcache/
       160     dir hibernate-testing/
       256     dir release/
       128     dir shared/
        96     dir hibernate-platform/
       128     dir hibernate-graalvm/
       128     dir hibernate-integrationtest-java-modules/
       448     dir gradle/
      7198    file README.adoc
       224     dir edb/
       128     dir hibernate-hikaricp/
        96     dir tck/
      8692    file gradlew
       128     dir hibernate-c3p0/
      1420    file dco.txt
      5741    file CONTRIBUTING.md
      4340    file build.gradle
     14579    file Jenkinsfile
       192     dir rules/
     73640    file changelog.txt
     26530    file lgpl.txt
      1623    file utilities.gradle
     13918    file nightly.Jenkinsfile
      4796    file migration-guide.adoc
      2026    file gradle.properties
      3911    file dialects.adoc
       128     dir hibernate-envers/
       128     dir hibernate-agroal/
       224     dir javadoc/
      2868    file gradlew.bat
     44538    file docker_db.sh
     18867    file settings.gradle
        96     dir patched-libs/
     10157    file test-case-guide.adoc
"""

async def single_test(ask_this, *, tools_must_be):
    messages: [chat_client.Message] = [
        chat_client.Message(role="system", content=SYSTEM_PROMPT),
        chat_client.Message(role="user", content=LOCATION),
        # chat_client.Message(role="assistant", content='"""\nIt is about the current project, I will switch current directory.\n"""', tool_calls=[chat_client.ToolCallDict(id="call_oTSH5DQ3HFrGWaY53ZGIIjyT", type="function", function=chat_client.FunctionDict(name="cd", arguments="{\"path\":\"code_horrible/hibernate-orm\"}"))]),
        # chat_client.Message(role="tool", tool_call_id="call_oTSH5DQ3HFrGWaY53ZGIIjyT", content=LOCATION),
        chat_client.Message(role="user", content=ask_this),
    ]

    N = 1
    tools_turn_on = {"definition", "references", "file", "search_workspace"}
    tools = await chat_client.tools_fetch_and_filter(base_url="http://127.0.0.1:8001/v1", tools_turn_on=tools_turn_on)
    assistant_choices = await chat_client.ask_using_http(
        "http://127.0.0.1:8001/v1",
        messages,
        N,
        MODEL,
        tools=tools,
        verbose=False,
        temperature=0.3,
        stream=False,
        max_tokens=2048,
    )
    assert(len(assistant_choices)==N)
    messages = assistant_choices[0]
    bad = (not not messages[-1].tool_calls) != tools_must_be
    color = "red" if bad else "green"
    content = messages[-1].content if messages[-1].content else "no content"
    if messages[-1].tool_calls:
        # calls_str = ", ".join([x.function.name for x in messages[-1].tool_calls])
        calls_str = ""
        for call in messages[-1].tool_calls:
            calls_str += f" {call.function.name}({call.function.arguments})"
    else:
        calls_str = "no_calls"
    print("%s\n%s\n%s" % (ask_this.replace("\n", "\\n"), termcolor.colored(content.replace("\n", "\\n"), "blue"), termcolor.colored(calls_str, color)))


async def all_tests():
    print("model is %s" % MODEL)
    print("---- must be no calls ----")
    await single_test(ask_this="What is the meaning of life?", tools_must_be=False)
    await single_test(ask_this="What is your name?", tools_must_be=False)
    await single_test(ask_this="Explain string theory", tools_must_be=False)
    await single_test(ask_this="Write pygame example", tools_must_be=False)
    await single_test(ask_this="```\n@validator('input')\n```\nWhy is this outdated in fastapi?", tools_must_be=False)
    print("---- must be calls ----")
    await single_test(ask_this="What is Frog?", tools_must_be=True)
    await single_test(ask_this="Why is there type conversion service in this project?", tools_must_be=True)
    await single_test(ask_this="list methods of ConversionService", tools_must_be=True)
    await single_test(ask_this="explain `public class ReadableBytesTypeConverter implements FormattingTypeConverter<CharSequence, Number, ReadableBytes>`", tools_must_be=True)


if __name__ == "__main__":
    asyncio.run(all_tests())
