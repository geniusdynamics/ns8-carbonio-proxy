*** Settings ***
Library    SSHLibrary

*** Variables ***
${TEST_HOST}    webmail.ns8-ci.test

*** Test Cases ***
# The proxy joins a ns8-carbonio main server on another node: the single
# test node cannot run both (they share the IMAP/POP3 ports). The suite
# checks the installation, the validation and the removal.

Check if carbonio-proxy is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}

Check that the configuration requires a main server
    ${output}  ${rc} =    Execute Command
    ...    api-cli run module/${module_id}/configure-module --data '{"host":"${TEST_HOST}","lets_encrypt":false,"http2https":true}'
    ...    return_rc=True
    Should Not Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    join_required

Check that an unknown main server is refused
    ${output}  ${rc} =    Execute Command
    ...    api-cli run module/${module_id}/configure-module --data '{"host":"${TEST_HOST}","join":"carbonio99"}'
    ...    return_rc=True
    Should Not Be Equal As Integers    ${rc}  0
    Should Contain    ${output}    join_not_found

Check the configuration of a new proxy
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/get-configuration --data '{}'
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    ${config} =    Evaluate    json.loads('''${output}''')    modules=json
    Should Not Be True    ${config}[initialized]
    Should Be Equal    ${config}[available_masters]    ${{ [] }}
    Should Not Be Empty    ${config}[release]

Check that the state secrets are private
    ${output} =    Execute Command    stat -c %a /home/${module_id}/.config/state/secrets.env
    Should Be Equal As Strings    ${output}    600

Check the health of a stopped proxy
    ${output}  ${rc} =    Execute Command    api-cli run module/${module_id}/get-health --data '{}'
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    ${health} =    Evaluate    json.loads('''${output}''')    modules=json
    Should Not Be True    ${health}[service_active]

Check if carbonio-proxy is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
