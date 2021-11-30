def alert(message: str, form: str) -> str:
    """Renders alert message

    params:
        message (str) - the message to put into the alert
        form (str) - type of alert (refer to Bootstrap documentation)
            e.g. 'danger', 'warning', 'success'

    return: message is sent wrapped in warning html
    """
    return f"""
            <div class="alert alert-{form} role="alert">
                {message}
            </div>
            """


def err(ref: dict, names: dict) -> str:
    """Render error message

    param:
        ref (dict) - the request object as a dictionary
        names (dict) - the key pair of presentable name and name from html
            template

    returns: error message of missing values as an html string
    """
    err = [names[k] for k, v in ref.items() if not v]
    answer = alert(f"Missing Values: <b>{'</b>, <b>'.join(err)}</b>", "danger")
    return answer


def output_results(outputs: dict) -> str:
    """Renders results

    param:
        outputs (dict): the output of the results

    returns: resulting calculations in an html string
    """
    lst = []
    lst.append(
        """
                <table class="table table-striped table-hover"
                    <thead>
                    </thead>
                    <tbody>
                """
    )
    for k, v in outputs.items():
        lst.append(
            f"""
                    <tr>
                        <th scope="row">{k}:</th>
                        <td>{v: .2f} mmHg</td>
                    </tr>
                    """
        )
    lst.append(
        """
                    </tbody>
                </table>
               """
    )
    answer = "\n".join(lst)
    return answer
