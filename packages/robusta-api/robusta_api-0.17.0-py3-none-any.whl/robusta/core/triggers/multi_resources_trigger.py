from typing import Any, Dict, List

from robusta.core.playbooks.base_trigger import TriggerEvent
from robusta.integrations.kubernetes.autogenerated.triggers import KubernetesAnyAllChangesTrigger
from robusta.integrations.kubernetes.base_triggers import DEFAULT_CHANGE_FILTERS, K8sTriggerEvent
from robusta.utils.scope import ScopeParams


class MultiResourceTrigger(KubernetesAnyAllChangesTrigger):
    """
    Can be configured to fire on a set of Kubernetes resources, for all or a subset of operations

    :var resources: List of Kubernetes resources. If empty, all resources are included.
                    Allowed values: deployment, pod, job, node, replicaset, statefulset, daemonset, ingress, service,
                    event, horizontalpodautoscaler, clusterrole, clusterrolebinding, namespace, serviceaccount, persistentvolume, configmap
    :var operations: List of operations. If empty, all operations are included. Allowed values: create, update, delete

    :example resources: ["deployment", "job", "ingress"]
    :example operations: ["create", "update"]
    """

    resources: List[str] = (None,)
    operations: List[str] = None

    def __init__(
        self,
        name_prefix: str = None,
        namespace_prefix: str = None,
        labels_selector: str = None,
        resources: List[str] = None,
        operations: List[str] = None,
        change_filters: Dict[str, List[str]] = DEFAULT_CHANGE_FILTERS,
        scope: ScopeParams = None
    ):
        super().__init__(
            name_prefix=name_prefix,
            namespace_prefix=namespace_prefix,
            labels_selector=labels_selector,
            change_filters=change_filters,
            scope=scope
        )
        self.resources = [resource.lower() for resource in resources] if resources else []
        self.operations = [op.lower() for op in operations] if operations else []

    def should_fire(self, event: TriggerEvent, playbook_id: str, build_context: Dict[str, Any]):
        should_fire = super().should_fire(event, playbook_id, build_context)
        if not should_fire:
            return should_fire

        if not isinstance(event, K8sTriggerEvent):
            return False

        if self.resources and event.k8s_payload.kind.lower() not in self.resources:
            return False

        if self.operations and event.k8s_payload.operation.lower() not in self.operations:
            return False

        return True
