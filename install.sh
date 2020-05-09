
oc apply -f templates/*.yaml

oc adm policy add-scc-to-user privileged -z hosted-loadbalancer -n openshift-hosted-loadbalancer

